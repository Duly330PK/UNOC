/*
 * UNOC - main.js (v5 - WebSocket Client)
 */

// --- Globale Variablen & Zustand ---
const backendUrl = "http://127.0.0.1:5000";
let socket = null; // NEU: WebSocket-Instanz
let network = null, map = null, nodes = new vis.DataSet([]), edges = new vis.DataSet([]);
let mapMarkers = {}, mapLines = {}, currentView = 'topo', eventPollInterval = null; // eventPollInterval wird nicht mehr genutzt, aber bleibt zur Klarheit hier
let highlightedPath = { nodes: [], links: [] };

const statusToColor = {
    online: { border: "#4CAF50", background: "#2e7d32" }, offline: { border: "#F44336", background: "#c62828" },
    maintenance: { border: "#FFC107", background: "#ffa000" }, up: { color: "#4CAF50", highlight: "#66BB6A" },
    down: { color: "#F44336", highlight: "#EF5350" }, degraded: { color: "#FFC107", highlight: "#FFCA28" },
    blocking: { color: "#FFC107", highlight: "#FFCA28" }
};
const getEdgeLeafletColor = (status) => (statusToColor[status] || { color: '#9E9E9E' }).color;

// Angepasste formatDeviceToNode und formatLinkToEdge, um die '_str' IDs aus dem Backend zu verwenden
const formatDeviceToNode = d => ({id: d.device_id_str, label: `${d.type}\n(${d.device_id_str})`, shape: 'box', borderWidth: 1, color: statusToColor[d.status], font: { color: '#ffffff' }, data: d});
// l.source und l.target sind bereits die String-IDs im Backend-JSON (aus serialize_link)
const formatLinkToEdge = l => ({id: l.link_id_str, from: l.source, to: l.target, width: 1, color: (statusToColor[l.status] || {}).color, arrows: 'to, from', dashes: l.status === 'blocking' ? [5, 5] : false, data: l, label: l.link_id_str, font: { color: '#aaa', size: 11, align: 'top', strokeWidth: 3, strokeColor: '#1a1a1a' }});

// --- Initialisierung ---
async function initialize() {
    initializeWebSocket(); // NEU: WebSocket-Verbindung aufbauen
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
        nodes.add(data.devices.map(formatDeviceToNode));
        edges.add(data.links.map(formatLinkToEdge));

        // NEU: Network-Objekt HIER initialisieren, BEVOR Event Listener gesetzt werden
        if (!network) {
            const container = document.getElementById('network-container');
            network = new vis.Network(container, { nodes, edges }, { interaction: { hover: true } });
            setupEventListeners(); 
        } 
        
        updateRingPanel(data); 
        initializeMapView(data); 

        const splitterSelect = document.getElementById('splitter-select');
        splitterSelect.innerHTML = '';
        data.devices.filter(d => d.type.toLowerCase() === 'splitter').forEach(d => {
            const option = document.createElement('option');
            option.value = d.device_id_str; 
            option.textContent = d.device_id_str;
            splitterSelect.appendChild(option);
        });

        updateHud(data.stats); 
        updateHistoryButtons(data.history_status); 
    });

    socket.on('topology_update', (update) => {
        console.log("Update empfangen:", update);
        if (update.type === 'link') {
            // Stelle sicher, dass die Link-Objekte die Source/Target IDs als Strings haben
            edges.update(formatLinkToEdge(update.data));
            syncMapWithState({ links: [update.data] }); 
        } else if (update.type === 'device') {
            nodes.update(formatDeviceToNode(update.data));
            // Kartendarstellung für Geräte-Statusänderung (z.B. Markerfarbe ändern) wäre hier sinnvoll,
            // ist aber in Leaflet nicht direkt in formatDeviceToNode enthalten.
            // mapMarkers[update.data.device_id_str].setIcon(...) könnte hier benötigt werden,
            // aber das ist komplexer und außerhalb des aktuellen Scopes.
        }
    });

    socket.on('stats_update', (stats) => { 
        console.log("Stats Update empfangen:", stats);
        updateHud(stats);
    });

    socket.on('history_status_update', (status) => { 
        console.log("History Status Update empfangen:", status);
        updateHistoryButtons(status);
    });

    socket.on('new_event', (event_message) => {
        console.log("Neues Event empfangen:", event_message);
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
        console.log("Verbindung zum WebSocket-Server getrennt!");
        showModal('Verbindung getrennt', 'Verbindung zum Backend verloren. Bitte Seite neu laden.', [{ text: 'OK', class: 'modal-btn-danger', callback: () => window.location.reload() }]);
    });
}

function refreshTopologyDisplay(topologyData) {
    nodes.clear();
    edges.clear();
    nodes.add(topologyData.devices.map(formatDeviceToNode));
    edges.add(topologyData.links.map(formatLinkToEdge));
    updateRingPanel(topologyData);
    initializeMapView(topologyData); 
}

function initializeMapView(topology) {
    // Korrigierte Logik, um `map` nur einmal zu initialisieren
    if (!map) { 
        const mapContainer = document.getElementById('map-container');
        if (mapContainer) { 
            map = L.map(mapContainer).setView([51.96, 7.62], 10);
            // Tile Layer direkt hier zuweisen, bevor Marker/Lines hinzugefügt werden
            L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; OpenStreetMap &copy; CARTO', maxZoom: 20
            }).addTo(map);
        } else {
            console.error("Map container not found!");
            return;
        }
    } else {
        Object.values(mapMarkers).forEach(marker => marker.remove());
        Object.values(mapLines).forEach(line => line.remove());
        mapMarkers = {}; 
        mapLines = {};
    }

    topology.devices.forEach(device => { 
        if (device.coordinates) {
            // KORREKTUR: mapMarkers-Key und Popup-ID verwenden device.device_id_str
            mapMarkers[device.device_id_str] = L.marker(device.coordinates).addTo(map).bindPopup(`<b>${device.device_id_str}</b><br>${device.type}`); 
        }
    });
    topology.links.forEach(link => {
        // KORREKTUR: link.source und link.target sind jetzt bereits die String-IDs (vom Backend geliefert)
        const source = topology.devices.find(d => d.device_id_str === link.source); 
        const target = topology.devices.find(d => d.device_id_str === link.target); 
        if (source?.coordinates && target?.coordinates) {
            mapLines[link.link_id_str] = L.polyline([source.coordinates, target.coordinates], { color: getEdgeLeafletColor(link.status), weight: 3, dashArray: link.status === 'blocking' ? '5, 5' : null }).addTo(map);
        }
    });
}

function syncMapWithState(topology_partial) { 
    if (!map) return;
    topology_partial.links.forEach(link => {
        if (mapLines[link.link_id_str]) {
            mapLines[link.link_id_str].setStyle({ color: getEdgeLeafletColor(link.status), dashArray: link.status === 'blocking' ? '5, 5' : null });
        }
    });
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
    // WICHTIG: Ringe kommen jetzt aus der DB, deren Link-IDs auch _str
    if (!topology.rings?.length) { ringInfoDiv.innerHTML = '<span class="loader">Keine Ringe definiert.</span>'; return; }
    let html = '<table>';
    topology.rings.forEach(ring => {
        // KORREKTUR: Findet den Link über ring.rpl_link_id_str (das ist die String-ID vom Backend)
        const rpl = topology.links.find(l => l.link_id_str === ring.rpl_link_id_str); 
        if (rpl) {
            const statusClass = rpl.status === 'blocking' ? 'status-blocking' : 'status-forwarding';
            html += `<tr><td><b>${ring.name}</b></td><td class="${statusClass}">${rpl.status.toUpperCase()}</td></tr>`;
        }
    });
    ringInfoDiv.innerHTML = html + '</table>';
}

async function renderProperties(dataToShow) {
    const contentDiv = document.getElementById('properties-content');
    if (!dataToShow) { contentDiv.innerHTML = '<span class="loader">Kein Element ausgewählt</span>'; return; }
    let table = '<table>';
    for (const [k, v] of Object.entries(dataToShow)) {
        if (k === 'properties') continue;
        let displayValue = v;
        // WICHTIG: IDs sind jetzt device_id_str/link_id_str
        if (k === 'device_id_str') displayValue = v; // Display as 'id'
        else if (k === 'link_id_str') displayValue = v; // Display as 'id'
        else if (k === 'source') displayValue = v; // Link-Objekt im Frontend hat source (string ID)
        else if (k === 'target') displayValue = v; // Link-Objekt im Frontend hat target (string ID)
        else if (k === 'coordinates' && Array.isArray(v)) displayValue = `${v[0].toFixed(4)}, ${v[1].toFixed(4)}`;
        else if (typeof v === 'object' && v !== null) displayValue = JSON.stringify(v);
        // KORREKTUR: 'id' wird schon als 'Id' angezeigt, also k.replace('_str', '') für die anderen '_str' Felder
        table += `<tr><th style="text-transform: capitalize;">${k.replace('_str', '').replace('_id', ' ID')}</th><td>${displayValue}</td></tr>`; 
    }
    table += '</table>';

    if (dataToShow.properties && Object.keys(dataToShow.properties).length > 0) {
        table += `<h3 style="text-align:center; background-color: #333; margin: 15px 0 0; padding: 8px;">Properties</h3>`;
        table += `<table>`;
        for (const [propKey, propValue] of Object.entries(dataToShow.properties)) {
             table += `<tr><th style="padding-left: 20px;">${propKey}</th><td>${propValue}</td></tr>`;
        }
        table += `</table>`;
    }
    contentDiv.innerHTML = table;


    // WICHTIG: Type ist jetzt in dataToShow.type
    if (dataToShow.type === 'ONT') { // dataToShow.type ist jetzt direkt verfügbar
        try {
            // KORREKTUR: ID für API-Call ist jetzt dataToShow.id (die Frontend-ID, die device_id_str ist)
            const response = await fetch(`${backendUrl}/api/devices/${dataToShow.id}/signal`); 
            if (!response.ok) return;
            const signalInfo = await response.json();
            if (!signalInfo || signalInfo.status === 'NOT_APPLICABLE') return;
            const signalRow = document.createElement('tr');
            let signalCellHTML = '';
            if (signalInfo.status === 'NO_PATH') {
                signalCellHTML = `<td class="signal-los" colspan="2">${signalInfo.status} (Pfad unterbrochen)</td>`;
            } else if (signalInfo.power_dbm !== null) {
                const signalStatusClass = `signal-${signalInfo.status.toLowerCase()}`;
                signalCellHTML = `<td class="${signalStatusClass}" colspan="2">${signalInfo.power_dbm} dBm (${signalInfo.status})</td>`;
            }
            if (signalCellHTML) {
                const tableElement = contentDiv.querySelector('table');
                if (tableElement) tableElement.innerHTML += `<tr><th style="text-align:center;" colspan="2">Signal Level</th></tr><tr>${signalCellHTML}</tr>`;
            }
        } catch (e) { console.error("Fehler beim Abrufen des Signalpegels:", e); }
    }
}

function toggleView() {
    const mapContainer = document.getElementById('map-container');
    const toggleBtn = document.getElementById('toggle-btn');
    const isTopo = currentView === 'topo';
    mapContainer.style.visibility = isTopo ? 'visible' : 'hidden';
    toggleBtn.textContent = isTopo ? 'Topologieansicht' : 'Kartenansicht';
    currentView = isTopo ? 'map' : 'topo';
    if (isTopo) map.invalidateSize();
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
        button.onclick = () => { hideModal(); if (btnInfo.callback) btnInfo.callback(); };
        buttonContainer.appendChild(button);
    });
    document.getElementById('modal-overlay').classList.remove('hidden');
}

function hideModal() { document.getElementById('modal-overlay').classList.add('hidden'); }

function setupEventListeners() {
    network.on('click', params => {
        if (params.nodes.length === 0 && params.edges.length === 0) {
            setTimeout(() => resetHighlight(), 0);
        }
        const elementId = params.nodes[0] || params.edges[0]; // ID kommt jetzt als device_id_str / link_id_str
        const dataset = params.nodes.length ? nodes : edges;
        renderProperties(elementId ? dataset.get(elementId).data : null);
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
        if (document.getElementById('cli-suggestions') && !document.getElementById('cli-interaction-area').contains(e.target)) {
            clearSuggestions();
        }
    });
}

async function postAction(endpoint, payload = {}) {
    // Diese Funktion sendet weiterhin HTTP-POST-Anfragen, um Aktionen auszulösen.
    // Die *Antwort* (also das Update) kommt aber über den WebSocket.
    try {
        const res = await fetch(`${backendUrl}${endpoint}`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        if (!res.ok) { const errorData = await res.json(); throw new Error(errorData.description || "Unbekannter Backend-Fehler"); }
        // Hier wurde 'pollForUpdates()' entfernt und durch die WebSocket-Updates ersetzt.
        // Bei 'load' Snapshots muss weiterhin die initialize() Funktion aufgerufen werden,
        // da dies einen kompletten Reset des Frontend-Zustands erfordert, der vom Backend
        // via 'initial_topology' WebSocket-Event gesendet wird.
        if (endpoint.includes('load')) {
             // Da initialize() die WebSocket-Verbindung neu aufbaut und initial_topology anfordert,
             // ist dies der korrekte Weg, den Frontend-Zustand nach einem Snapshot-Load zu aktualisieren.
             initialize(); 
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
    if (nodeId) showModal('Faserschnitt simulieren', `Soll ein Faserschnitt bei <strong>${nodeId}</strong> wirklich simuliert werden?`, [{ text: 'Abbrechen', class: 'modal-btn-secondary' }, { text: 'Simulieren', class: 'modal-btn-danger', callback: () => postAction('/api/simulation/fiber-cut', { node_id: nodeId }) }]);
    else showModal('Fehler', 'Bitte einen Splitter für den Faserschnitt auswählen.');
}
function saveSnapshot() {
    const name = document.getElementById('snapshot-name').value.trim();
    if (name) postAction('/api/snapshot/save', { name });
    else showModal('Fehler', 'Bitte einen Namen für den Snapshot eingeben.');
}
function loadSnapshot() {
    const name = document.getElementById('snapshot-name').value.trim();
    if (name) showModal('Snapshot laden', `Soll der Snapshot '<strong>${name}</strong>' wirklich geladen werden?`, [{ text: 'Abbrechen', class: 'modal-btn-secondary' }, { text: 'Laden', class: 'modal-btn-primary', callback: () => postAction('/api/snapshot/load', { name }) }]);
    else showModal('Fehler', 'Bitte den Namen des zu ladenden Snapshots eingeben.');
}

const KNOWN_COMMANDS = ['help', 'undo', 'redo', 'cut', 'fiber-cut', 'link-down', 'link-up', 'link-degraded', 'trace'];
function debounce(func, delay) { let timeout; return function(...args) { clearTimeout(timeout); timeout = setTimeout(() => func.apply(this, args), delay); }; }
function showCliOutput(message, type = 'info') {
    const cliOutput = document.getElementById('cli-output');
    if(!cliOutput) return;
    const colorMap = { error: 'var(--accent-red)', warning: '#FFC107', 'info': 'var(--text-color)' }; 
    cliOutput.innerHTML += `<div>${message}</div>`;
    cliOutput.querySelector('div:last-child').style.color = colorMap[type] || colorMap.info;
    cliOutput.scrollTop = cliOutput.scrollHeight;
}

async function handleCliCommand(inputElement) {
    const commandStr = inputElement.value.trim();
    if (!commandStr) return;
    showCliOutput(`<span style="color: var(--text-muted);">UNOC></span> ${commandStr}`);
    const [command, ...args] = commandStr.split(' ');
    inputElement.value = ''; clearSuggestions();
    if (command === 'trace') { await tracePath(args[0], args[1]); return; }
    if (command === "help") { showCliOutput(`Verfügbare Befehle: ${KNOWN_COMMANDS.join(', ')}`, 'info'); }
    else if (command === "undo") { await postAction('/api/simulation/undo'); }
    else if (command === "redo") { await postAction('/api/simulation/redo'); }
    else if (command === "cut" || command === "fiber-cut") { await postAction('/api/simulation/fiber-cut', { node_id: args[0] }); }
    else if (["link-down", "link-up", "link-degraded"].includes(command)) { await postAction(`/api/links/${args[0]}/status`, { status: command.split("-")[1] }); }
    else { showCliOutput(`Unbekannter Befehl: '${command}'.`, 'error'); }
}

async function tracePath(startNode, endNode) {
    resetHighlight();
    if (!startNode || !endNode) { showCliOutput("Fehler: `trace` benötigt Start- und Endknoten. Bsp: trace NODE-A NODE-B", 'error'); return; }
    try {
        const response = await fetch(`${backendUrl}/api/simulation/trace-path`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ start_node: startNode, end_node: endNode }) });
        if (!response.ok) { const error = await response.json(); throw new Error(error.description || "Unbekannter Backend-Fehler"); }
        const path = await response.json();
        if (path.nodes.length === 0) { showCliOutput(`Kein aktiver Pfad zwischen ${startNode} und ${endNode} gefunden.`, 'warning'); }
        else {
            highlightedPath = { nodes: path.nodes, links: path.links };
            // WICHTIG: nodes und edges IDs sind jetzt string IDs
            nodes.update(path.nodes.map(id => ({ id, borderWidth: 3, color: { border: '#00BFFF' } })));
            edges.update(path.links.map(id => ({ id, width: 4, color: '#00BFFF' })));
            showCliOutput(`Pfad gefunden: ${path.nodes.join(' -> ')}`);
        }
    } catch (e) { showCliOutput(`Fehler bei der Pfadverfolgung: ${e.message}`, 'error'); }
}

function resetHighlight() {
    if (highlightedPath.nodes.length === 0 && highlightedPath.links.length === 0) return;
    const nodesToUpdate = nodes.get(highlightedPath.nodes);
    const edgesToUpdate = edges.get(highlightedPath.links);
    if (nodesToUpdate.length > 0) {
        // Sicherstellen, dass formatDeviceToNode das korrekte Datenformat erhält
        const nodeResets = nodesToUpdate.map(node => { const defaultStyle = formatDeviceToNode(node.data); return { id: node.id, borderWidth: defaultStyle.borderWidth, color: defaultStyle.color }; });
        nodes.update(nodeResets);
    }
    if (edgesToUpdate.length > 0) {
        const edgeResets = edgesToUpdate.map(edge => { const defaultStyle = formatLinkToEdge(edge.data); return { id: edge.id, width: defaultStyle.width, color: defaultStyle.color }; });
        edges.update(edgeResets);
    }
    highlightedPath = { nodes: [], links: [] };
}

function handleCliKeyDown(event) {
    const suggestions = document.querySelectorAll('.suggestion-item');
    let activeIndex = -1;
    suggestions.forEach((s, i) => { if (s.classList.contains('active')) activeIndex = i; });
    if (event.key === 'Enter') {
        event.preventDefault();
        if (activeIndex > -1) { suggestions[activeIndex].click(); }
        else { handleCliCommand(event.target); }
    } else if (event.key === 'ArrowDown') {
        event.preventDefault();
        if (activeIndex < suggestions.length - 1) { if (activeIndex > -1) suggestions[activeIndex].classList.remove('active'); suggestions[activeIndex + 1].classList.add('active'); }
    } else if (event.key === 'ArrowUp') {
        event.preventDefault();
        if (activeIndex > 0) { suggestions[activeIndex].classList.remove('active'); suggestions[activeIndex - 1].classList.add('active'); }
    } else if (event.key === 'Escape') { clearSuggestions(); }
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
        // KORREKTUR: Greife auf item.id zu, da diese die string ID ist
        if (currentPartIndex === 1) { suggestions = edges.get({ filter: item => item.id.toLowerCase().startsWith(partial.toLowerCase()) }).map(item => item.id); }
    } else if (commandsWithNodeIds.includes(command)) {
        // KORREKTUR: Greife auf item.id zu
        if (currentPartIndex === 1 || (command === 'trace' && currentPartIndex === 2)) {
            const existingNodes = parts.slice(1, currentPartIndex);
            suggestions = nodes.get({ filter: item => !existingNodes.includes(item.id) && item.id.toLowerCase().startsWith(partial.toLowerCase()) }).map(item => item.id);
        }
    }
    renderSuggestions(suggestions, baseCommand);
}

function renderSuggestions(suggestions, baseCommand) {
    const container = document.getElementById('cli-suggestions');
    if (suggestions.length === 0) { clearSuggestions(); return; }
    container.innerHTML = suggestions.map(s => `<div class="suggestion-item" onclick="selectSuggestion('${baseCommand}', '${s}')">${s}</div>`).join('');
}

function selectSuggestion(baseCommand, id) {
    const inputElement = document.getElementById('cli-input');
    inputElement.value = (baseCommand ? `${baseCommand} ` : '') + `${id} `;
    inputElement.focus();
    inputElement.dispatchEvent(new Event('keyup', { bubbles: true }));
}

function clearSuggestions() {
    const container = document.getElementById('cli-suggestions');
    if(container) container.innerHTML = '';
}

function resetHighlight() {
    if (network) {
        network.unselectAll();
    }

    selectedDevice = null;
    selectedLink = null;

    renderProperties(null);  // Setzt die rechte Sidebar zurück
    console.log("Highlight reset");
}

document.addEventListener('DOMContentLoaded', initialize);