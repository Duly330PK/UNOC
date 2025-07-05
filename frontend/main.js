/*
 * UNOC - main.js (v6 - GeoJSON & Zoom-Logik Integration)
 */

// --- Globale Variablen & Zustand ---
const backendUrl = "http://127.0.0.1:5000";
let socket = null;
let network = null, map = null, nodes = new vis.DataSet([]), edges = new vis.DataSet([]);
let mapMarkers = {}, mapLines = {}, currentView = 'topo';
let highlightedPath = { nodes: [], links: [] };
let selectedId = null;
let selectedType = null; // 'device' oder 'link'

// NEU: Konfiguration für die Kartenansicht
const ZOOM_THRESHOLD = 7; // Ab welchem Zoom-Level werden regionale Details sichtbar?

const statusToColor = {
    online: { border: "#4CAF50", background: "#2e7d32" },
    offline: { border: "#F44336", background: "#c62828" },
    maintenance: { border: "#FFC107", background: "#ffa000" },
    up: { color: "#4CAF50", highlight: "#66BB6A" },
    down: { color: "#F44336", highlight: "#EF5350" },
    degraded: { color: "#FFC107", highlight: "#FFCA28" },
    blocking: { color: "#FFC107", highlight: "#FFCA28" }
};

const getEdgeLeafletColor = (status) => (statusToColor[status] || { color: '#9E9E9E' }).color;

// --- Formatierungsfunktionen ---

function formatDeviceToNode(d) {
    const node = {
        id: d.id, // ID ist jetzt die device_id_str
        label: d.type === 'POP' || d.type === 'Core Node' ? d.id : `${d.type}\n(${d.id})`,
        shape: 'box',
        borderWidth: 1,
        color: statusToColor[d.status],
        font: { color: '#ffffff' },
        data: d,
    };

    // Spezifische Stile für neue Typen
    if (d.type === 'Core Node') {
        node.shape = 'database';
        node.color = { border: '#00BFFF', background: '#202A40' };
        node.size = 25;
        node.font = { color: '#00BFFF', size: 14 };
    } else if (d.type === 'POP') {
        node.shape = 'box';
        node.color = { border: '#8A2BE2', background: '#301934' };
    }

    return node;
}

function formatLinkToEdge(l) {
    const edge = {
        id: l.id, // ID ist jetzt die link_id_str
        from: l.source,
        to: l.target,
        width: 2, // Standardbreite
        color: (statusToColor[l.status] || {}).color || '#9E9E9E',
        arrows: 'to, from',
        dashes: l.status === 'blocking' ? [5, 5] : false,
        data: l,
        label: l.properties?.typ,
        font: { color: '#aaa', size: 11, align: 'top', strokeWidth: 3, strokeColor: '#1a1a1a' }
    };

    // NEU: Logik zur Überschreibung der Stile für Backbone- und Regional-Links
    const props = l.properties;
    if (props && props.typ) {
        if (props.typ === 'Backbone') {
            edge.color = { color: '#FF4500' }; // Orangered
            edge.width = 4;
            edge.dashes = [10, 10];
            edge.label = 'Backbone';
        } else if (props.typ === 'Regional') {
            edge.color = { color: '#8A2BE2' }; // BlueViolet
            edge.width = 2.5;
            edge.dashes = [5, 5];
            edge.label = 'Regional';
        }
    }
    return edge;
}

// --- Initialisierung ---
async function initialize() {
    initializeWebSocket();
}

function initializeWebSocket() {
    socket = io(backendUrl);

    socket.on('connect', () => {
        console.log("Verbunden mit dem WebSocket-Server!");
        socket.emit('request_initial_data');
    });

    socket.on('initial_topology', (data) => {
        console.log("Initiale Topologie empfangen:", data);
        
        nodes.clear();
        edges.clear();
        
        const formattedNodes = data.devices.map(d => formatDeviceToNode({ ...d, id: d.id }));
        const formattedEdges = data.links.map(l => formatLinkToEdge({ ...l, id: l.id }));

        nodes.add(formattedNodes);
        edges.add(formattedEdges);

        if (!network) {
            const container = document.getElementById('network-container');
            network = new vis.Network(container, { nodes, edges }, { interaction: { hover: true } });
            setupEventListeners();
        }
        
        if(data.rings) updateRingPanel(data);
        initializeMapView(data);

        const splitterSelect = document.getElementById('splitter-select');
        splitterSelect.innerHTML = '';
        data.devices.filter(d => d.type.toLowerCase() === 'splitter').forEach(d => {
            const option = document.createElement('option');
            option.value = d.id;
            option.textContent = d.id;
            splitterSelect.appendChild(option);
        });

        if (data.stats) updateHud(data.stats);
        if (data.history_status) updateHistoryButtons(data.history_status);
        if (data.alarms) updateAlarms(data.alarms);
    });

    socket.on('full_state_update', (data) => {
        console.log("Full State Update empfangen:", data);
        
        const updatedNodes = data.devices.map(d => formatDeviceToNode({ ...d, id: d.id }));
        nodes.update(updatedNodes);

        const updatedLinks = data.links.map(l => formatLinkToEdge({ ...l, id: l.id }));
        edges.update(updatedLinks);

        updateHud(data.stats);
        updateHistoryButtons(data.history_status);
        updateRingPanel(data);
        updateAlarms(data.alarms);
        syncMapWithState(data);

        if (selectedId) {
            const selectedData = data.devices.find(d => d.id === selectedId) || data.links.find(l => l.id === selectedId);
            if (selectedData) renderProperties(selectedData);
        }
    });
    
    socket.on('new_event', (event_message) => {
        const eventLog = document.getElementById('event-log');
        const newLi = document.createElement('li');
        newLi.textContent = event_message;
        if (eventLog.firstChild && eventLog.firstChild.classList.contains('loader')) {
            eventLog.innerHTML = '';
        }
        eventLog.prepend(newLi);
        while (eventLog.children.length > 100) {
            eventLog.removeChild(eventLog.lastChild);
        }
    });

    socket.on('disconnect', () => {
        showModal('Verbindung getrennt', 'Verbindung zum Backend verloren. Bitte Seite neu laden.', [{ text: 'OK', class: 'modal-btn-danger', callback: () => window.location.reload() }]);
    });
}

// --- UI-Update-Funktionen ---

function updateAlarms(alarms) {
    const hudAlarms = document.getElementById('hud-alarms');
    hudAlarms.textContent = alarms ? alarms.length : 0;
    hudAlarms.style.color = (alarms && alarms.length > 0) ? 'var(--accent-red)' : 'var(--accent-green)';

    nodes.update(nodes.getIds().map(id => ({ id, icon: undefined })));

    if (alarms) {
        alarms.forEach(alarm => {
            if (alarm.affected_object_type === 'device') {
                nodes.update({
                    id: alarm.affected_object_id,
                    icon: { face: "'Font Awesome 5 Free'", code: '\uf071', size: 50, color: 'red' }
                });
            }
        });
    }
}

function updateHud(stats) {
    document.getElementById('hud-devices').textContent = `${stats.devices_online} / ${stats.devices_total}`;
    document.getElementById('hud-links').textContent = `${stats.links_up} / ${stats.links_total}`;
    const alarmsEl = document.getElementById('hud-alarms');
    alarmsEl.textContent = stats.alarms;
    alarmsEl.style.color = stats.alarms > 0 ? 'var(--accent-red)' : 'var(--accent-green)';
}

function updateHistoryButtons(status) {
    document.getElementById('undo-btn').disabled = !status.can_undo;
    document.getElementById('redo-btn').disabled = !status.can_redo;
}

function updateRingPanel(topology) {
    const ringInfoDiv = document.getElementById('ring-info');
    if (!topology.rings || !topology.rings.length) {
        ringInfoDiv.innerHTML = '<span class="loader">Keine Ringe definiert.</span>';
        return;
    }
    let html = '<table>';
    topology.rings.forEach(ring => {
        const rpl = topology.links.find(l => l.id === ring.rpl_link_id);
        if (rpl) {
            const statusClass = rpl.status === 'blocking' ? 'status-blocking' : 'status-forwarding';
            html += `<tr><td><b>${ring.name}</b></td><td class="${statusClass}">${rpl.status.toUpperCase()}</td></tr>`;
        }
    });
    ringInfoDiv.innerHTML = html + '</table>';
}

// --- Karten- & Zoom-Logik ---

// --- Karten- & Zoom-Logik ---

function initializeMapView(topology) {
    if (!map) {
        const mapContainer = document.getElementById('map-container');
        if (mapContainer) {
            map = L.map(mapContainer).setView([51.5, 10.5], 6); // Start-Zoom auf Deutschland
            L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; OpenStreetMap &copy; CARTO', maxZoom: 20
            }).addTo(map);

            map.on('zoomend', handleZoom);
        } else {
            console.error("Map container not found!");
            return;
        }
    }
    
    Object.values(mapMarkers).forEach(marker => marker.remove());
    Object.values(mapLines).forEach(line => line.remove());
    mapMarkers = {};
    mapLines = {};

    // Erstellt die Marker und fügt den Klick-Handler hinzu
    topology.devices.forEach(device => {
        if (device.coordinates && device.coordinates.length === 2) {
            const marker = L.marker([device.coordinates[1], device.coordinates[0]])
                .addTo(map)
                .bindPopup(`<b>${device.id}</b><br>${device.type}`);

            // Klick-Event-Handler für den Marker hinzugefügt
            marker.on('click', () => {
                selectedId = device.id;
                selectedType = 'device';
                renderProperties(device);
                if (network) {
                    network.selectNodes([device.id]);
                }
            });

            mapMarkers[device.id] = marker;
        }
    });

    // Erstellt die Linien zwischen den Markern
    topology.links.forEach(link => {
        const source = topology.devices.find(d => d.id === link.source);
        const target = topology.devices.find(d => d.id === link.target);
        if (source?.coordinates && target?.coordinates) {
            const latlngs = [
                [source.coordinates[1], source.coordinates[0]],
                [target.coordinates[1], target.coordinates[0]]
            ];
            mapLines[link.id] = L.polyline(latlngs).addTo(map);
        }
    });

    // Diese Aufrufe gehören an das Ende von initializeMapView
    syncMapWithState(topology);
    handleZoom();
} // <-- Die Funktion initializeMapView endet hier.


// Die folgenden Funktionen sind jetzt korrekt außerhalb definiert.
function syncMapWithState(topology) {
    if (!map) return;
    
    topology.links.forEach(link => {
        if (mapLines[link.id]) {
            const props = link.properties;
            let style = { color: getEdgeLeafletColor(link.status), weight: 2 };

            if (props?.typ === 'Backbone') {
                style.weight = 5;
                style.color = '#FF4500';
                style.dashArray = '15, 15';
            } else if (props?.typ === 'Regional') {
                style.weight = 3;
                style.color = '#8A2BE2';
                style.dashArray = '8, 8';
            } else if (link.status === 'blocking') {
                style.dashArray = '5, 5';
            }
            
            mapLines[link.id].setStyle(style);
        }
    });
}

function handleZoom() {
    if (!map) return;
    const zoomLevel = map.getZoom();

    for (const deviceId in mapMarkers) {
        const marker = mapMarkers[deviceId];
        const node = nodes.get(deviceId);
        if (!node) continue;
        
        if (node.data.type === 'Core Node') {
            marker.setOpacity(1); // Core Nodes sind immer sichtbar.
        } else {
            marker.setOpacity(zoomLevel > ZOOM_THRESHOLD ? 1 : 0);
        }
    }

    for (const linkId in mapLines) {
        const line = mapLines[linkId];
        const edge = edges.get(linkId);
        if (!edge) continue;

        if (edge.data.properties?.typ === 'Backbone') {
            line.setStyle({ opacity: 1 }); // Backbone-Links sind immer sichtbar.
        } else {
            line.setStyle({ opacity: zoomLevel > ZOOM_THRESHOLD ? 1 : 0 });
        }
    }
}
// --- Eigenschaften-Panel & Interaktion ---

async function renderProperties(dataToShow) {
    const contentDiv = document.getElementById('properties-content');
    if (!dataToShow) {
        contentDiv.innerHTML = '<span class="loader">Kein Element ausgewählt</span>';
        return;
    }

    let table = '<table>';
    // Basis-Eigenschaften
    table += `<tr><th>ID</th><td>${dataToShow.id}</td></tr>`;
    table += `<tr><th>Typ</th><td>${dataToShow.type}</td></tr>`;
    if (dataToShow.status) table += `<tr><th>Status</th><td>${dataToShow.status}</td></tr>`;

    // NEU: Spezifische Anzeige für Core Nodes
    if (dataToShow.type === 'Core Node') {
        const props = dataToShow.properties;
        table += '</table><h3 style="text-align:center; background-color: #333; margin: 15px 0 0; padding: 8px;">Core Network Details</h3><table>';
        table += `<tr><th>Standort</th><td>${props.standort || 'N/A'}</td></tr>`;
        table += `<tr><th>Peering</th><td>${props.peering || 'N/A'}</td></tr>`;
        table += `<tr><th>Kapazität</th><td>${props.peering_capacity_gbit || 'N/A'} Gbit/s</td></tr>`;
        table += `<tr><th>AS-Nummern</th><td>${props.as_numbers || 'N/A'}</td></tr>`;
    } 
    // Anzeige der generischen Properties
    else if (dataToShow.properties && Object.keys(dataToShow.properties).length > 0) {
        table += '</table><h3 style="text-align:center; background-color: #333; margin: 15px 0 0; padding: 8px;">Properties</h3><table>';
        for (const [propKey, propValue] of Object.entries(dataToShow.properties)) {
            table += `<tr><th>${propKey}</th><td>${JSON.stringify(propValue)}</td></tr>`;
        }
    }
    table += '</table>';

    contentDiv.innerHTML = table;
    
    // Signalpegel-Logik für ONTs
    if (dataToShow.type === 'ONT') {
        try {
            const response = await fetch(`${backendUrl}/api/devices/${dataToShow.id}/signal`);
            if (!response.ok) return;
            const signalInfo = await response.json();
            if (!signalInfo || signalInfo.status === 'NOT_APPLICABLE') return;

            let signalCellHTML = '';
            if (signalInfo.status === 'NO_PATH') {
                signalCellHTML = `<td class="signal-los" colspan="2">${signalInfo.status} (Pfad unterbrochen)</td>`;
            } else if (signalInfo.power_dbm !== null) {
                const signalStatusClass = `signal-${signalInfo.status.toLowerCase()}`;
                signalCellHTML = `<td class="${signalStatusClass}" colspan="2">${signalInfo.power_dbm} dBm (${signalInfo.status})</td>`;
            }

            if (signalCellHTML) {
                const tableElement = contentDiv.querySelector('table');
                if (tableElement) {
                    // Find the last table to append to
                    const tables = contentDiv.querySelectorAll('table');
                    const lastTable = tables[tables.length - 1];
                    lastTable.innerHTML += `<tr><th style="text-align:center;" colspan="2">Signal Level</th></tr><tr>${signalCellHTML}</tr>`;
                }
            }
        } catch (e) {
            console.error("Fehler beim Abrufen des Signalpegels:", e);
        }
    }
}


function toggleView() {
    const mapContainer = document.getElementById('map-container');
    const networkContainer = document.getElementById('network-container');
    const toggleBtn = document.getElementById('toggle-btn');
    
    if (currentView === 'topo') {
        mapContainer.style.visibility = 'visible';
        networkContainer.style.visibility = 'hidden';
        toggleBtn.textContent = 'Topologieansicht';
        currentView = 'map';
        if (map) map.invalidateSize(); // Wichtig, damit die Karte korrekt gerendert wird
    } else {
        mapContainer.style.visibility = 'hidden';
        networkContainer.style.visibility = 'visible';
        toggleBtn.textContent = 'Kartenansicht';
        currentView = 'topo';
    }
}

function showModal(title, message, buttons = [{ text: 'OK', class: 'modal-btn-primary', callback: hideModal }]) {
    document.getElementById('modal-title').textContent = title;
    document.getElementById('modal-message').innerHTML = message;
    const buttonContainer = document.getElementById('modal-buttons');
    buttonContainer.innerHTML = '';
    buttons.forEach(btnInfo => {
        const button = document.createElement('button');
        button.textContent = btnInfo.text;
        button.className = btnInfo.class || 'modal-btn-secondary';
        button.onclick = () => {
            hideModal();
            if (btnInfo.callback) btnInfo.callback();
        };
        buttonContainer.appendChild(button);
    });
    document.getElementById('modal-overlay').classList.remove('hidden');
}

function hideModal() {
    document.getElementById('modal-overlay').classList.add('hidden');
}

function setupEventListeners() {
    network.on('click', params => {
        const elementId = params.nodes[0] || params.edges[0];
        if (elementId) {
            selectedId = elementId;
            selectedType = params.nodes.length ? 'device' : 'link';
            const dataSet = selectedType === 'device' ? nodes : edges;
            const itemData = dataSet.get(selectedId);
            if (itemData) {
                 renderProperties(itemData.data || itemData); // data-Attribut bei gruppierten Nodes
            }
        } else {
            selectedId = null;
            selectedType = null;
            renderProperties(null);
            resetHighlight();
        }
    });

    document.getElementById('toggle-btn').addEventListener('click', toggleView);
    document.getElementById('undo-btn').addEventListener('click', () => postAction('/api/simulation/undo'));
    document.getElementById('redo-btn').addEventListener('click', () => postAction('/api/simulation/redo'));
    document.getElementById('reset-highlight-btn').addEventListener('click', resetHighlight);
    document.getElementById('fiber-cut-btn').addEventListener('click', simulateFiberCut);
    document.getElementById('save-snapshot-btn').addEventListener('click', saveSnapshot);
    document.getElementById('load-snapshot-btn').addEventListener('click', loadSnapshot);
    document.getElementById('cli-input').addEventListener('keydown', handleCliKeyDown);
    document.getElementById('cli-input').addEventListener('keyup', debounce(handleAutocomplete, 250));

    document.addEventListener('click', (e) => {
        if (document.getElementById('cli-suggestions') &&
            !document.getElementById('cli-interaction-area').contains(e.target)) {
            clearSuggestions();
        }
    });
}

// --- Aktionen & CLI ---

async function postAction(endpoint, payload = {}) {
    try {
        const res = await fetch(`${backendUrl}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const contentType = res.headers.get("content-type");
        if (!res.ok) {
            if (contentType && contentType.includes("application/json")) {
                const errorData = await res.json();
                throw new Error(errorData.description || "Unbekannter Backend-Fehler");
            } else {
                const errorText = await res.text();
                console.error("Fehlerhafte Antwort (kein JSON):", errorText);
                throw new Error("Unerwartete Server-Antwort (kein JSON)");
            }
        }

        if (endpoint.includes('/api/snapshot/load')) {
            // Nach dem Laden eines Snapshots, fordern wir die neuen Daten an
            socket.emit('request_initial_data');
        }

        return true;
    } catch (error) {
        console.error("Aktion fehlgeschlagen:", error);
        showModal('Aktion fehlgeschlagen', error.message);
        return false;
    }
}

function simulateFiberCut() {
    const nodeId = document.getElementById('splitter-select').value;
    if (nodeId) {
        showModal(
            'Faserschnitt simulieren',
            `Soll ein Faserschnitt bei <strong>${nodeId}</strong> wirklich simuliert werden?`,
            [
                { text: 'Abbrechen', class: 'modal-btn-secondary' },
                { text: 'Simulieren', class: 'modal-btn-danger', callback: () => postAction('/api/simulation/fiber-cut', { node_id: nodeId }) }
            ]
        );
    } else {
        showModal('Fehler', 'Bitte einen Splitter für den Faserschnitt auswählen.');
    }
}

function saveSnapshot() {
    const name = document.getElementById('snapshot-name').value.trim();
    if (name) {
        postAction('/api/snapshot/save', { name });
    } else {
        showModal('Fehler', 'Bitte einen Namen für den Snapshot eingeben.');
    }
}

function loadSnapshot() {
    const name = document.getElementById('snapshot-name').value.trim();
    if (name) {
        showModal(
            'Snapshot laden',
            `Soll der Snapshot '<strong>${name}</strong>' wirklich geladen werden?`,
            [
                { text: 'Abbrechen', class: 'modal-btn-secondary' },
                { text: 'Laden', class: 'modal-btn-primary', callback: () => postAction('/api/snapshot/load', { name }) }
            ]
        );
    } else {
        showModal('Fehler', 'Bitte den Namen des zu ladenden Snapshots eingeben.');
    }
}

const KNOWN_COMMANDS = [
    'help', 'undo', 'redo', 'cut', 'fiber-cut',
    'link-down', 'link-up', 'link-degraded',
    'trace', 'link-util'
];

function debounce(func, delay) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
    };
}

function showCliOutput(message, type = 'info') {
    const cliOutput = document.getElementById('cli-output');
    if (!cliOutput) return;
    const colorMap = {
        error: 'var(--accent-red)',
        warning: '#FFC107',
        info: 'var(--text-color)'
    };
    cliOutput.innerHTML += `<div>${message}</div>`;
    cliOutput.querySelector('div:last-child').style.color = colorMap[type] || colorMap.info;
    cliOutput.scrollTop = cliOutput.scrollHeight;
}

async function handleCliCommand(inputElement) {
    const commandStr = inputElement.value.trim();
    if (!commandStr) return;
    showCliOutput(`<span style="color: var(--text-muted);">UNOC></span> ${commandStr}`);

    const [command, ...args] = commandStr.split(' ');
    inputElement.value = '';
    clearSuggestions();

    if (command === 'trace') {
        await tracePath(args[0], args[1]);
        return;
    }
    if (command === "help") {
        showCliOutput(`Verfügbare Befehle: ${KNOWN_COMMANDS.join(', ')}`, 'info');
    } else if (command === "undo") {
        await postAction('/api/simulation/undo');
    } else if (command === "redo") {
        await postAction('/api/simulation/redo');
    } else if (command === "cut" || command === "fiber-cut") {
        await postAction('/api/simulation/fiber-cut', { node_id: args[0] });
    } else if (["link-down", "link-up", "link-degraded"].includes(command)) {
        await postAction(`/api/links/${args[0]}/status`, { status: command.split("-")[1] });
    } else if (command === "link-util") {
        if (!args[0] || !args[1] || isNaN(Number(args[1]))) {
            showCliOutput("Usage: link-util <link-id> <percent>", "error");
            return;
        }
        await postAction(`/api/links/${args[0]}/utilization`, { utilization: Number(args[1]) });
    } else {
        showCliOutput(`Unbekannter Befehl: '${command}'.`, 'error');
    }
}

async function tracePath(startNode, endNode) {
    resetHighlight();
    if (!startNode || !endNode) {
        showCliOutput("Fehler: `trace` benötigt Start- und Endknoten. Bsp: trace NODE-A NODE-B", 'error');
        return;
    }
    try {
        const response = await fetch(`${backendUrl}/api/simulation/trace-path`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ start_node: startNode, end_node: endNode })
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.description || "Unbekannter Backend-Fehler");
        }
        const path = await response.json();
        if (path.nodes.length === 0) {
            showCliOutput(`Kein aktiver Pfad zwischen ${startNode} und ${endNode} gefunden.`, 'warning');
        } else {
            highlightedPath = { nodes: path.nodes, links: path.links };
            nodes.update(path.nodes.map(id => ({ id, borderWidth: 3, color: { border: '#00BFFF' } })));
            edges.update(path.links.map(id => ({ id, width: 4, color: '#00BFFF' })));
            showCliOutput(`Pfad gefunden: ${path.nodes.join(' -> ')}`);
        }
    } catch (e) {
        showCliOutput(`Fehler bei der Pfadverfolgung: ${e.message}`, 'error');
    }
}

function resetHighlight() {
    if (highlightedPath.nodes.length === 0 && highlightedPath.links.length === 0) return;

    const nodesToUpdate = nodes.get(highlightedPath.nodes);
    const edgesToUpdate = edges.get(highlightedPath.links);

    if (nodesToUpdate.length > 0) {
        const nodeResets = nodesToUpdate.map(node => {
            const defaultStyle = formatDeviceToNode(node.data);
            return {
                id: node.id,
                borderWidth: defaultStyle.borderWidth,
                color: defaultStyle.color
            };
        });
        nodes.update(nodeResets);
    }

    if (edgesToUpdate.length > 0) {
        const edgeResets = edgesToUpdate.map(edge => {
            const defaultStyle = formatLinkToEdge(edge.data);
            return {
                id: edge.id,
                width: defaultStyle.width,
                color: defaultStyle.color
            };
        });
        edges.update(edgeResets);
    }

    highlightedPath = { nodes: [], links: [] };
}

function handleCliKeyDown(event) {
    const suggestions = document.querySelectorAll('.suggestion-item');
    let activeIndex = -1;
    suggestions.forEach((s, i) => {
        if (s.classList.contains('active')) activeIndex = i;
    });

    if (event.key === 'Enter') {
        event.preventDefault();
        if (activeIndex > -1) {
            suggestions[activeIndex].click();
        } else {
            handleCliCommand(event.target);
        }
    } else if (event.key === 'ArrowDown') {
        event.preventDefault();
        if (activeIndex < suggestions.length - 1) {
            if (activeIndex > -1) suggestions[activeIndex].classList.remove('active');
            suggestions[activeIndex + 1].classList.add('active');
        }
    } else if (event.key === 'ArrowUp') {
        event.preventDefault();
        if (activeIndex > 0) {
            suggestions[activeIndex].classList.remove('active');
            suggestions[activeIndex - 1].classList.add('active');
        }
    } else if (event.key === 'Escape') {
        clearSuggestions();
    }
}

function handleAutocomplete(event) {
    const text = event.target.value;
    const parts = text.split(' ');
    const command = parts[0];
    const currentPartIndex = parts.length - 1;
    const partial = parts[currentPartIndex];

    if (currentPartIndex === 0) {
        const suggestions = KNOWN_COMMANDS.filter(c => c.startsWith(partial));
        renderSuggestions(suggestions, "");
        return;
    }

    const baseCommand = parts.slice(0, currentPartIndex).join(' ');
    let suggestions = [];

    const commandsWithNodeIds = ['cut', 'fiber-cut', 'trace'];
    const commandsWithLinkIds = ['link-down', 'link-up', 'link-degraded'];

    if (commandsWithLinkIds.includes(command)) {
        if (currentPartIndex === 1) {
            suggestions = edges.get({
                filter: item => item.id.toLowerCase().startsWith(partial.toLowerCase())
            }).map(item => item.id);
        }
    } else if (commandsWithNodeIds.includes(command)) {
        if (currentPartIndex === 1 || (command === 'trace' && currentPartIndex === 2)) {
            const existingNodes = parts.slice(1, currentPartIndex);
            suggestions = nodes.get({
                filter: item =>
                    !existingNodes.includes(item.id) &&
                    item.id.toLowerCase().startsWith(partial.toLowerCase())
            }).map(item => item.id);
        }
    }

    renderSuggestions(suggestions, baseCommand);
}

function renderSuggestions(suggestions, baseCommand) {
    const container = document.getElementById('cli-suggestions');
    if (!container || suggestions.length === 0) {
        clearSuggestions();
        return;
    }
    container.innerHTML = suggestions.map(s =>
        `<div class="suggestion-item" onclick="selectSuggestion('${baseCommand}', '${s}')">${s}</div>`
    ).join('');
}

function selectSuggestion(baseCommand, id) {
    const inputElement = document.getElementById('cli-input');
    inputElement.value = (baseCommand ? `${baseCommand} ` : '') + `${id} `;
    inputElement.focus();
    clearSuggestions();
}

function clearSuggestions() {
    const container = document.getElementById('cli-suggestions');
    if (container) container.innerHTML = '';
}

// --- Start ---
document.addEventListener('DOMContentLoaded', initialize);