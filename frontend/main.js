const backendUrl = "http://127.0.0.1:5000";
let network = null, map = null, nodes = new vis.DataSet([]), edges = new vis.DataSet([]);
let mapMarkers = {}, mapLines = {}, currentView = 'topo', eventPollInterval = null;
let highlightedPath = { nodes: [], links: [] };

const statusToColor = {
    online: { border: "#4CAF50", background: "#2e7d32" }, offline: { border: "#F44336", background: "#c62828" },
    maintenance: { border: "#FFC107", background: "#ffa000" }, up: { color: "#4CAF50", highlight: "#66BB6A" },
    down: { color: "#F44336", highlight: "#EF5350" }, degraded: { color: "#FFC107", highlight: "#FFCA28" },
    blocking: { color: "#FFC107", highlight: "#FFCA28" }
};
const getEdgeLeafletColor = (status) => (statusToColor[status] || { color: '#9E9E9E' }).color;

const formatDeviceToNode = d => ({id: d.id, label: `${d.type}\n(${d.id})`, shape: 'box', borderWidth: 1, color: statusToColor[d.status], font: { color: '#ffffff' }, data: d});
const formatLinkToEdge = l => ({id: l.id, from: l.source, to: l.target, width: 1, color: (statusToColor[l.status] || {}).color, arrows: 'to, from', dashes: l.status === 'blocking' ? [5, 5] : false, data: l, label: l.id, font: { color: '#aaa', size: 11, align: 'top', strokeWidth: 3, strokeColor: '#1a1a1a' }});

async function initialize() {
    try {
        const response = await fetch(`${backendUrl}/api/topology`);
        if (!response.ok) throw new Error(`Backend nicht erreichbar: ${response.statusText}`);
        const topology = await response.json();
        
        const splitterSelect = document.getElementById('splitter-select');
        splitterSelect.innerHTML = '';
        topology.devices.filter(d => d.type.toLowerCase() === 'splitter').forEach(d => {
            const option = document.createElement('option');
            option.value = d.id;
            option.textContent = d.id;
            splitterSelect.appendChild(option);
        });

        if (!network) {
            const container = document.getElementById('network-container');
            network = new vis.Network(container, { nodes, edges }, { interaction: { hover: true } });
        }
         if (!map) {
            map = L.map('map-container').setView([51.96, 7.62], 10);
            L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; OpenStreetMap &copy; CARTO', maxZoom: 20
            }).addTo(map);
        }

        refreshTopologyDisplay(topology);
        
        if (!eventPollInterval) {
            setupEventListeners();
            pollForUpdates();
            eventPollInterval = setInterval(pollForUpdates, 2500);
        }
    } catch (e) { 
        console.error("Fehler bei der Initialisierung:", e);
        const container = document.getElementById('network-container');
        container.innerHTML = `<p style="color: var(--accent-red); padding: 20px;">Verbindung zum Backend fehlgeschlagen. Läuft der Server auf ${backendUrl}?</p>`;
    }
}

async function pollForUpdates() {
    try {
        const [eventsRes, historyRes, statsRes, topoRes] = await Promise.all([
            fetch(`${backendUrl}/api/events`), fetch(`${backendUrl}/api/history/status`),
            fetch(`${backendUrl}/api/topology/stats`), fetch(`${backendUrl}/api/topology`)
        ]);
        
        if (!eventsRes.ok || !historyRes.ok || !statsRes.ok || !topoRes.ok) throw new Error("Backend nicht erreichbar");

        const events = await eventsRes.json();
        const historyStatus = await historyRes.json();
        const stats = await statsRes.json();
        const topology = await topoRes.json();
        
        document.getElementById('event-log').innerHTML = events.map(e => `<li>${e}</li>`).join('');
        updateHud(stats);
        updateHistoryButtons(historyStatus);

        if (highlightedPath.nodes.length === 0) {
            nodes.update(topology.devices.map(formatDeviceToNode));
            edges.update(topology.links.map(formatLinkToEdge));
        }
        updateRingPanel(topology);
        syncMapWithState(topology);
    } catch (error) { console.error("Polling-Fehler:", error); }
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
    if(map){
        Object.values(mapMarkers).forEach(marker => marker.remove());
        Object.values(mapLines).forEach(line => line.remove());
        mapMarkers = {}; mapLines = {};
    }
    topology.devices.forEach(device => { if (device.coordinates) mapMarkers[device.id] = L.marker(device.coordinates).addTo(map).bindPopup(`<b>${device.id}</b><br>${device.type}`); });
    topology.links.forEach(link => {
        const source = topology.devices.find(d => d.id === link.source);
        const target = topology.devices.find(d => d.id === link.target);
        if (source?.coordinates && target?.coordinates) {
            mapLines[link.id] = L.polyline([source.coordinates, target.coordinates], { color: getEdgeLeafletColor(link.status), weight: 3, dashArray: link.status === 'blocking' ? '5, 5' : null }).addTo(map);
        }
    });
}

function syncMapWithState(topology) {
    if (!map) return;
    topology.links.forEach(link => {
        if (mapLines[link.id]) {
            mapLines[link.id].setStyle({ color: getEdgeLeafletColor(link.status), dashArray: link.status === 'blocking' ? '5, 5' : null });
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
    if (!topology.rings?.length) { ringInfoDiv.innerHTML = '<span class="loader">Keine Ringe definiert.</span>'; return; }
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

async function renderProperties(dataToShow) {
    const contentDiv = document.getElementById('properties-content');
    if (!dataToShow) { contentDiv.innerHTML = '<span class="loader">Kein Element ausgewählt</span>'; return; }
    let table = '<table>';
    for (const [k, v] of Object.entries(dataToShow)) {
        if (k === 'properties') continue;
        let displayValue = v;
        if (k === 'coordinates' && Array.isArray(v)) displayValue = `${v[0].toFixed(4)}, ${v[1].toFixed(4)}`;
        else if (typeof v === 'object' && v !== null) displayValue = JSON.stringify(v);
        table += `<tr><th style="text-transform: capitalize;">${k}</th><td>${displayValue}</td></tr>`;
    }
    if (dataToShow.properties && Object.keys(dataToShow.properties).length > 0) {
        table += `<tr><th colspan="2" style="text-align:center; background-color: #333;">Properties</th></tr>`;
        for (const [propKey, propValue] of Object.entries(dataToShow.properties)) {
             table += `<tr><th style="padding-left: 20px;">${propKey}</th><td>${propValue}</td></tr>`;
        }
    }
    table += '</table>';
    contentDiv.innerHTML = table;
    if (dataToShow.type === 'ONT') {
        try {
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
        const elementId = params.nodes[0] || params.edges[0];
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
    try {
        const res = await fetch(`${backendUrl}${endpoint}`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        if (!res.ok) { const errorData = await res.json(); throw new Error(errorData.description || "Unbekannter Backend-Fehler"); }
        if (endpoint.includes('load')) { await initialize(); } 
        else { await pollForUpdates(); }
    } catch (error) {
        console.error("Aktion fehlgeschlagen:", error);
        showModal('Aktion fehlgeschlagen', error.message);
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
    const colorMap = { error: 'var(--accent-red)', warning: '#FFC107', info: 'var(--text-color)' };
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
        if (!response.ok) { const error = await response.json(); throw new Error(error.description || "Unbekannter Fehler bei der Pfadsuche"); }
        const path = await response.json();
        if (path.nodes.length === 0) { showCliOutput(`Kein aktiver Pfad zwischen ${startNode} und ${endNode} gefunden.`, 'warning'); }
        else {
            highlightedPath = { nodes: path.nodes, links: path.links };
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
        if (currentPartIndex === 1) { suggestions = edges.get({ filter: item => item.id.toLowerCase().startsWith(partial.toLowerCase()) }).map(item => item.id); }
    } else if (commandsWithNodeIds.includes(command)) {
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

document.addEventListener('DOMContentLoaded', initialize);