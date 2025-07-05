/*
 * UNOC - main.js (v10 - L2/L3 Simulation für Phase 5)
 */

// --- Globale Variablen & Zustand ---
const backendUrl = "http://127.0.0.1:5000";
let socket = null;
let network = null, map = null, nodes = new vis.DataSet([]), edges = new vis.DataSet([]);
let mapMarkers = {}, mapLines = {}, currentView = 'topo';
let highlightedPath = { nodes: [], links: [] };
let selectedId = null;
let selectedType = null;

let fullTopologyData = null; // Speichert die komplette, ungefilterte Topologie
let activeViewMode = 'national'; // Startet mit der nationalen Ansicht

let currentArchFilter = 'all'; // Mögliche Werte: 'all', 'PON', 'PtP'
const END_DEVICE_TYPES = ['ONT', 'Business NT']; // Hilfskonstante

const ZOOM_THRESHOLD = 7; 

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
        id: d.id,
        label: d.type,
        title: `${d.type}: ${d.id}`,
        shape: 'box',
        borderWidth: 2,
        color: statusToColor[d.status] || { border: '#9E9E9E', background: '#616161' },
        font: { color: '#ffffff' },
        data: d,
    };

    switch (d.type) {
        case 'Core Node':
            node.shape = 'database';
            node.color = { border: '#00BFFF', background: '#202A40' };
            node.size = 30;
            node.label = d.id;
            break;
        case 'POP':
            node.shape = 'database';
            node.color = { border: '#FFFFFF', background: '#007BFF' };
            node.size = 25;
            node.label = d.id;
            break;
        case 'ODF':
            node.label = 'ODF';
            node.color = { border: '#cccccc', background: '#555555' };
            break;
        case 'NVt':
            node.color = { border: '#cccccc', background: '#888888' };
            break;
        case 'HÜP':
            node.shape = 'dot';
            node.size = 10;
            node.label = null;
            break;
        case 'OLT':
            node.color = { border: '#f5b041', background: '#873600' };
            break;
        case 'Splitter':
            node.color = { border: '#a569bd', background: '#5b2c6f' };
            break;
        case 'AON Switch':
            node.shape = 'square';
            node.color = { border: '#9400D3', background: '#4B0082' };
            break;
        case 'Business NT':
            node.shape = 'box';
            node.color = { border: '#9400D3', background: '#4B0082' };
            node.label = "Business NT"
            break;
        case 'ONT':
             node.shape = 'box';
             node.color = statusToColor[d.status];
             break;
    }
    return node;
}

function formatLinkToEdge(l) {
    const edge = {
        id: l.id,
        from: l.source,
        to: l.target,
        width: 2,
        color: (statusToColor[l.status] || {}).color || '#9E9E9E',
        arrows: 'to, from',
        dashes: l.status === 'blocking' ? [5, 5] : false,
        data: l,
        font: { color: '#aaa', size: 11, align: 'top', strokeWidth: 3, strokeColor: '#1a1a1a' }
    };

    const props = l.properties || {};

    if (props.link_technology === 'PtP') {
        edge.color = { color: '#9400D3' };
        edge.width = 4;
        edge.dashes = false;
        edge.label = `PtP (${props.guaranteed_bandwidth_gbps || '...'} Gbit/s)`;
    } else if (props.typ === 'Backbone') {
        edge.color = { color: '#FF4500' };
        edge.width = 4;
        edge.dashes = [10, 10];
        edge.label = 'Backbone';
    } else if (props.typ === 'Regional') {
        edge.color = { color: '#8A2BE2' };
        edge.width = 2.5;
        edge.dashes = [5, 5];
        edge.label = 'Regional';
    }
    return edge;
}

// --- setupEventListeners (angepasst für Phase 5) ---
function setupEventListeners() {
    // Geografischer Ansicht-Umschalter
    document.getElementById('btn-view-national').addEventListener('click', () => renderView('national'));
    document.getElementById('btn-view-local').addEventListener('click', () => renderView('local'));

    // Toggle zwischen Karten- und Topologieansicht
    document.getElementById('toggle-btn').addEventListener('click', toggleView);

    // Klick auf das vis.js Netzwerk
    if (network) {
        network.on('click', params => {
            const nodeId = params.nodes.length > 0 ? params.nodes[0] : null;
            if (nodeId) {
                renderProperties(nodes.get(nodeId).data);
            } else {
                renderProperties(null);
            }
        });
    }

    // Architektur-Filter
    document.getElementById('filter-all').addEventListener('click', () => applyArchFilter('all'));
    document.getElementById('filter-pon').addEventListener('click', () => applyArchFilter('PON'));
    document.getElementById('filter-ptp').addEventListener('click', () => applyArchFilter('PtP'));

    // --- NEU FÜR PHASE 5: Virtueller Router ---
    document.getElementById('vr-apply-btn').addEventListener('click', applyVirtualRouterConfig);

    // CLI, Snapshots, Undo/Redo bleiben gleich
    document.getElementById('cli-input')?.addEventListener('keydown', handleCliKeyDown);
    document.getElementById('save-snapshot-btn')?.addEventListener('click', saveSnapshot);
    document.getElementById('load-snapshot-btn')?.addEventListener('click', loadSnapshot);
    document.getElementById('simulate-fiber-cut-btn')?.addEventListener('click', simulateFiberCut);
    document.getElementById('undo-btn')?.addEventListener('click', () => postAction('/api/simulation/undo'));
    document.getElementById('redo-btn')?.addEventListener('click', () => postAction('/api/simulation/redo'));
}

// --- Initialisierung & WebSocket (angepasst für Phase 5) ---
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
        console.log("Initiale Topologie empfangen.", data);
        fullTopologyData = data;
        renderView(activeViewMode);
    });

    socket.on('full_state_update', (data) => {
        console.log("Full State Update empfangen.");
        fullTopologyData = data;
        renderView(activeViewMode);
    });
    
    socket.on('new_event', (event_message) => {
        const eventLog = document.getElementById('event-log');
        const newLi = document.createElement('li');
        newLi.textContent = event_message;
        if (eventLog.firstChild && eventLog.firstChild.classList.contains('loader')) eventLog.innerHTML = '';
        eventLog.prepend(newLi);
        if (eventLog.children.length > 100) eventLog.removeChild(eventLog.lastChild);
    });

    // --- NEU FÜR PHASE 5: WebSocket-Handler für den Router-Status ---
    socket.on('virtual_router_status', (data) => {
        const output = document.getElementById('vr-status-output');
        if (!output) return;

        if (data.status === 'CONNECTED') {
            output.innerHTML = `
                <p style="color: var(--accent-green);">Status: Verbunden</p>
                <p>IPv4: ${data.ipv4.address} (${data.ipv4.type})</p>
                <p>IPv6: ${data.ipv6.prefix} (Angefordert: /${data.ipv6.delegated_size})</p>
            `;
            if (data.ipv6.delegated_size != 56) {
                output.innerHTML += `<p style="color: var(--accent-red);">WARNUNG: Subnetting nicht möglich!</p>`;
            }
        } else {
            output.innerHTML = `
                <p style="color: var(--accent-red);">Status: Fehlgeschlagen</p>
                <p>Grund: ${data.reason}</p>
            `;
        }
    });

    socket.on('disconnect', () => {
        showModal('Verbindung getrennt', 'Verbindung zum Backend verloren. Bitte Seite neu laden.', [{ text: 'OK', class: 'modal-btn-danger', callback: () => window.location.reload() }]);
    });
}

// --- Filter- & Rendering-Logik ---
function applyArchFilter(tech) {
    console.log(`Architektur-Filter wird auf "${tech}" gesetzt.`);
    currentArchFilter = tech;
    
    document.querySelectorAll('.arch-filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.getElementById(`filter-${tech.toLowerCase()}`).classList.add('active');

    renderView(activeViewMode);
}

function renderView(mode) {
    if (!fullTopologyData) return;

    activeViewMode = mode;
    console.log(`Rendering view: mode=${mode}, filter=${currentArchFilter}`);
    document.getElementById('btn-view-national').classList.toggle('active', mode === 'national');
    document.getElementById('btn-view-local').classList.toggle('active', mode === 'local');

    let geoFilteredData;
    if (mode === 'national') {
        const nationalDeviceIds = new Set(fullTopologyData.devices.filter(d => d.properties?.data_source === 'geojson').map(d => d.id));
        geoFilteredData = {
            devices: fullTopologyData.devices.filter(d => nationalDeviceIds.has(d.id)),
            links: fullTopologyData.links.filter(l => nationalDeviceIds.has(l.source) && nationalDeviceIds.has(l.target)),
            rings: fullTopologyData.rings || []
        };
    } else {
        const localDeviceIds = new Set(fullTopologyData.devices.filter(d => d.properties?.data_source === 'rees_topology').map(d => d.id));
        geoFilteredData = {
            devices: fullTopologyData.devices.filter(d => localDeviceIds.has(d.id)),
            links: fullTopologyData.links.filter(l => localDeviceIds.has(l.source) && localDeviceIds.has(l.target)),
            rings: (fullTopologyData.rings || []).filter(r => r.id.includes("REES"))
        };
    }

    let finalFilteredData = { devices: [], links: [] };
    if (currentArchFilter === 'all') {
        finalFilteredData.links = geoFilteredData.links;
    } else {
        finalFilteredData.links = geoFilteredData.links.filter(l => {
            const tech = l.properties?.link_technology || 'PON';
            return tech.toLowerCase() === currentArchFilter.toLowerCase();
        });
    }

    const visibleNodeIds = new Set();
    finalFilteredData.links.forEach(link => {
        visibleNodeIds.add(link.source);
        visibleNodeIds.add(link.target);
    });
    geoFilteredData.devices.forEach(d => {
       if (!edges.getIds().some(edgeId => edges.get(edgeId).from === d.id || edges.get(edgeId).to === d.id)) {
           if (finalFilteredData.links.length === 0 && currentArchFilter === 'all') {
               visibleNodeIds.add(d.id);
           }
       }
    });
    finalFilteredData.devices = geoFilteredData.devices.filter(device => visibleNodeIds.has(device.id));
    
    nodes.clear();
    edges.clear();
    nodes.add(finalFilteredData.devices.map(d => formatDeviceToNode(d)));
    edges.add(finalFilteredData.links.map(l => formatLinkToEdge(l)));
    
    if (!network) {
        const container = document.getElementById('network-container');
        const options = { 
            physics: {
                barnesHut: {
                    gravitationalConstant: -4000,
                    springLength: 250,
                    springConstant: 0.05,
                    avoidOverlap: 0.1
                }
            },
            interaction: { hover: true }
        };
        network = new vis.Network(container, { nodes, edges }, options);
        setupEventListeners();
    }
    
    initializeMapView(finalFilteredData);
    updateRingPanel(geoFilteredData);

    if (fullTopologyData.stats) updateHud(fullTopologyData.stats);
    if (fullTopologyData.alarms) updateAlarms(fullTopologyData.alarms);
    if (fullTopologyData.history_status) updateHistoryButtons(fullTopologyData.history_status);
    
    const mapContainer = document.getElementById('map-container');
    const networkContainer = document.getElementById('network-container');
    const toggleBtn = document.getElementById('toggle-btn');
    if (mode === 'national') {
        mapContainer.style.visibility = 'visible';
        networkContainer.style.visibility = 'hidden';
        toggleBtn.textContent = 'Topologieansicht';
        currentView = 'map';
        if (map) map.invalidateSize();
    } else {
        mapContainer.style.visibility = 'hidden';
        networkContainer.style.visibility = 'visible';
        toggleBtn.textContent = 'Kartenansicht';
        currentView = 'topo';
    }
}

// --- UI-Update-Funktionen ---
function updateAlarms(alarms) {
    const hudAlarms = document.getElementById('hud-alarms');
    hudAlarms.textContent = alarms ? alarms.length : 0;
    hudAlarms.style.color = (alarms && alarms.length > 0) ? 'var(--accent-red)' : 'var(--accent-green)';

    const activeAlarmedNodes = new Set(
        (alarms || [])
        .filter(a => a.affected_object_type === 'device')
        .map(a => a.affected_object_id)
    );

    nodes.getIds().forEach(nodeId => {
        const node = nodes.get(nodeId);
        const hasIcon = node && node.icon;
        const shouldHaveIcon = activeAlarmedNodes.has(nodeId);

        if (hasIcon && !shouldHaveIcon) {
            nodes.update({ id: nodeId, icon: undefined });
        } else if (!hasIcon && shouldHaveIcon) {
            nodes.update({
                id: nodeId,
                icon: { face: "'Font Awesome 5 Free'", code: '\uf071', size: 50, color: 'red' }
            });
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
    if (!topology.rings || !topology.rings.length) {
        ringInfoDiv.innerHTML = '<span class="loader">Keine Ringe definiert.</span>';
        return;
    }
    let html = '<table>';
    topology.rings.forEach(ring => {
        const rpl = fullTopologyData.links.find(l => l.id === ring.rpl_link_id);
        if (rpl) {
            const statusClass = rpl.status === 'blocking' ? 'status-blocking' : 'status-forwarding';
            html += `<tr><td><b>${ring.name}</b></td><td class="${statusClass}">${rpl.status.toUpperCase()}</td></tr>`;
        }
    });
    ringInfoDiv.innerHTML = html + '</table>';
}


// --- Karten- & Zoom-Logik ---
function initializeMapView(topology) {
    if (!map) {
        const mapContainer = document.getElementById('map-container');
        if (mapContainer) {
            map = L.map(mapContainer).setView([51.5, 10.5], 6);
            L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                attribution: '© OpenStreetMap © CARTO', maxZoom: 20
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

    topology.devices.forEach(device => {
        if (device.coordinates && device.coordinates.length === 2) {
            const marker = L.marker([device.coordinates[1], device.coordinates[0]])
                .addTo(map)
                .bindPopup(`<b>${device.id}</b><br>${device.type}`);
            marker.on('click', () => {
                selectedId = device.id;
                selectedType = 'device';
                renderProperties(device);
                if (network) { network.selectNodes([device.id]); }
            });
            mapMarkers[device.id] = marker;
        }
    });

    topology.links.forEach(link => {
        const source = fullTopologyData.devices.find(d => d.id === link.source);
        const target = fullTopologyData.devices.find(d => d.id === link.target);
        if (source?.coordinates && target?.coordinates) {
            const latlngs = [ [source.coordinates[1], source.coordinates[0]], [target.coordinates[1], target.coordinates[0]] ];
            mapLines[link.id] = L.polyline(latlngs).addTo(map);
        }
    });

    syncMapWithState(topology);
    handleZoom();
}

function syncMapWithState(topology) {
    if (!map) return;
    topology.links.forEach(link => {
        if (mapLines[link.id]) {
            const props = link.properties || {};
            let style = { color: getEdgeLeafletColor(link.status), weight: 2 };
            
            if (props.link_technology === 'PtP') {
                style.weight = 4;
                style.color = '#9400D3';
            } else if (props.typ === 'Backbone') { 
                style.weight = 5; style.color = '#FF4500'; style.dashArray = '15, 15';
            } else if (props.typ === 'Regional') { 
                style.weight = 3; style.color = '#8A2BE2'; style.dashArray = '8, 8';
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
            marker.setOpacity(1); 
        } else {
            marker.setOpacity(zoomLevel > ZOOM_THRESHOLD ? 1 : 0);
        }
    }

    for (const linkId in mapLines) {
        const line = mapLines[linkId];
        const edge = edges.get(linkId);
        if (!edge) continue;

        if (edge.data.properties?.typ === 'Backbone') {
            line.setStyle({ opacity: 1 });
        } else {
            line.setStyle({ opacity: zoomLevel > ZOOM_THRESHOLD ? 1 : 0 });
        }
    }
}

// --- Eigenschaften-Panel (angepasst für Phase 4) ---

async function renderProperties(dataToShow) {
    const contentDiv = document.getElementById('properties-content');
    if (!dataToShow) {
        contentDiv.innerHTML = '<span class="loader">Kein Element ausgewählt</span>';
        return;
    }

    let table = '<table>';
    table += `<tr><th>ID</th><td>${dataToShow.id}</td></tr>`;
    table += `<tr><th>Typ</th><td>${dataToShow.type}</td></tr>`;
    if (dataToShow.status) table += `<tr><th>Status</th><td>${dataToShow.status}</td></tr>`;
    table += '</table>';

    if (dataToShow.properties && Object.keys(dataToShow.properties).length > 0) {
        table += '<hr><h4>Eigenschaften</h4><table>';
        for (const [propKey, propValue] of Object.entries(dataToShow.properties)) {
            if (propKey === 'data_source') continue;
            table += `<tr><th>${propKey}</th><td>${JSON.stringify(propValue)}</td></tr>`;
        }
        table += '</table>';
    }
    contentDiv.innerHTML = table;
    
    // Logik für alle Endgeräte (ONT & Business NT)
    if (END_DEVICE_TYPES.includes(dataToShow.type)) {
        try {
            const res = await fetch(`${backendUrl}/api/devices/${dataToShow.id}/signal`);
            if (!res.ok) throw new Error(`Signalabfrage fehlgeschlagen: ${res.status}`);
            const signalInfo = await res.json();
            
            if (signalInfo.budget && signalInfo.power_dbm !== null) {
                let budgetHtml = `<hr><h4>Leistungsbudget-Analyse (${signalInfo.path_technology || ''})</h4><table>`;
                
                const txPowerKey = Object.keys(signalInfo.budget).find(k => k.toLowerCase().includes('transmit power'));
                if (txPowerKey) {
                    budgetHtml += `<tr><th>${txPowerKey}</th><td>${signalInfo.budget[txPowerKey].toFixed(2)} dBm</td></tr>`;
                }
                
                for (const [key, value] of Object.entries(signalInfo.budget)) {
                    if (key.toLowerCase().includes('transmit power')) continue;
                    if (key === 'Splitter Loss' && value === 0) continue;
                    
                    budgetHtml += `<tr><th>${key}</th><td>-${value.toFixed(2)} dB</td></tr>`;
                }

                const statusClass = signalInfo.status === 'online' ? 'signal-good' : `signal-${signalInfo.status.toLowerCase()}`;
                
                budgetHtml += `
                    <tr style="border-top: 2px solid #555;">
                        <th>Gesamtverlust</th><td>-${signalInfo.total_loss.toFixed(2)} dB</td>
                    </tr>
                    <tr>
                        <th>Empfangspegel (Rx)</th>
                        <td class="${statusClass}">${signalInfo.power_dbm.toFixed(2)} dBm</td>
                    </tr>
                `;
                budgetHtml += '</table>';
                contentDiv.innerHTML += budgetHtml;
            } else {
                const firstTable = contentDiv.querySelector('table');
                if (firstTable) {
                    const row = document.createElement('tr');
                    const statusText = signalInfo.status || (signalInfo.error || "N/A");
                    row.innerHTML = `<th>Signal Level</th><td class="signal-los">${statusText}</td>`;
                    firstTable.appendChild(row);
                }
            }
        } catch (e) {
            console.error("Fehler beim Abrufen des Signalpegels:", e);
        }
    }
}


// --- UI & Aktionen ---

function toggleView() {
    const mapContainer = document.getElementById('map-container');
    const networkContainer = document.getElementById('network-container');
    const toggleBtn = document.getElementById('toggle-btn');
    
    if (currentView === 'topo') {
        mapContainer.style.visibility = 'visible';
        networkContainer.style.visibility = 'hidden';
        toggleBtn.textContent = 'Topologieansicht';
        currentView = 'map';
        if (map) map.invalidateSize();
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
            socket.emit('request_initial_data');
        }

        return true;
    } catch (error) {
        console.error("Aktion fehlgeschlagen:", error);
        showModal('Aktion fehlgeschlagen', error.message);
        return false;
    }
}

// --- NEU FÜR PHASE 5: Logik zum Anwenden der Router-Konfiguration ---
function applyVirtualRouterConfig() {
    const config = {
        wan_type: document.getElementById('vr-wan-type').value,
        vlan_tag: document.getElementById('vr-vlan-tag').value || null,
        pd_size_request: parseInt(document.getElementById('vr-pd-size').value, 10)
    };
    
    // Setze den leeren VLAN-Tag auf null, um Konsistenz mit dem Backend zu gewährleisten
    if (config.vlan_tag === "") {
        config.vlan_tag = null;
    }

    console.log("Sende virtuelle Router-Konfiguration ans Backend:", config);
    postAction('/api/simulation/virtual-router/config', config);
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