Dokument-Version: 1.0
Datum: 04. Juli 2025
Ziel: Vollständige, ebenenübergreifende Emulation und Simulation der DG-Netzarchitektur, -protokolle und -dienste basierend auf den bereitgestellten Analysedokumenten.

Einleitung und Entwicklungsphilosophie
Dieses Dokument definiert die technischen Anforderungen zur Transformation des UNOC-Simulators in ein hochpräzises Abbild des Deutsche Glasfaser Netzes. Die Entwicklung folgt einer logischen Hierarchie, die sich an den Netzebenen orientiert – vom nationalen Backbone bis zum Endgerät des Kunden. Jede Phase baut auf der vorherigen auf, um eine konsistente und beherrschbare Implementierung zu gewährleisten. Das Ziel ist nicht nur die Simulation des fehlerfreien Betriebs, sondern explizit auch die Emulation von Konfigurationsfehlern und physikalischen Störungen, um ein wertvolles Werkzeug für Training, Analyse und Konfigurationsvalidierung zu schaffen.

Phase 1: Nationales Backbone und Core-Netzwerk (Netzebene 1/2)
In dieser Phase wird das übergeordnete Rückgrat des DG-Netzes modelliert. Das Verständnis dieses "Asset-light"-Ansatzes ist fundamental, da es die schnelle Expansion der DG erklärt und die primären Datenverkehrsrouten definiert.

Ziele:

Simulation der strategischen Abhängigkeit von Infrastrukturpartnern.

Visualisierung der nationalen Hauptverkehrsadern.

Genaue Verortung der primären Internet-Gateways.

Betroffene Simulationskomponenten:

Datenbank (database.py): Neue Modelle für Backbone-Provider und Core-Nodes.

Topologie-Engine (backend.py): Logik zur Darstellung von Partnernetzen.

Kartenansicht (main.js): Visualisierung der Backbone-Trassen.

Konkrete Umsetzungsschritte:

Modellierung der Partner-Backbones:


Beschreibung: Das DG-Backbone ist keine selbst gebaute Infrastruktur, sondern ein Kompositum aus angemieteten Dark-Fiber-Kapazitäten. Dies muss in der Simulation abgebildet werden.

Umsetzung:

Es werden zwei neue Link-Typen in der Simulation eingeführt: "GasLINE-Backbone" und "DB-Broadband-Backbone".

Diese Links werden visuell anders dargestellt (z.B. durch eine andere Farbe oder Strichart), um ihre Rolle als gemietete Infrastruktur zu verdeutlichen.

Die öffentlich zugänglichen Netzkarten von GasLINE und DB broadband GmbH werden als Vorlage genutzt, um die Haupttrassen zwischen den Metropolregionen auf der Simulationskarte nachzuzeichnen.

Implementierung der Core Network Nodes:


Beschreibung: Die DG konzentriert ihre Kernnetzinfrastruktur auf die primären Interconnection-Hubs in Frankfurt am Main, Düsseldorf und Amsterdam. An diesen Standorten wird der Datenverkehr mit dem globalen Internet ausgetauscht.

Umsetzung:

Die drei Core-Rechenzentren werden als hochpräzise, verifizierte Knotenpunkte in der Simulation angelegt.


Tabelle 4.1: Kernrechenzentren wird exakt in die Datenbank übernommen, inklusive Name, Adresse und Geokoordinaten.

Für jeden dieser Core Nodes werden die Peering-Informationen hinterlegt:


DE-CIX Frankfurt: Kapazität 400 Gbit/s.


MegaIX Dusseldorf: Kapazität 400 Gbit/s.


AMS-IX Amsterdam: Kapazität 100 Gbit/s.

Die relevanten AS-Nummern (AS60294 und AS8899) werden als Eigenschaft der Knoten gespeichert.

Visualisierung der nationalen Konnektivität:

Beschreibung: Die Kartenansicht muss die gesamte Hierarchie vom Core Node über das Partner-Backbone bis zu den regionalen Netzen darstellen.

Umsetzung:

Die UI erhält eine neue Zoom-abhängige Detailstufe. Bei einer deutschlandweiten Ansicht sind nur die Core Nodes und die Backbone-Trassen sichtbar.

Ein Klick auf einen Core Node zeigt die Peering-Partner und die verfügbare Kapazität an.

Ein Klick auf eine Backbone-Trasse zeigt den Eigentümer (GasLINE oder DB broadband) an.

Phase 2: Lokale Netzwerktopologie (Netzebene 3)
Diese Phase modelliert den Weg der Glasfaser vom zentralen Knotenpunkt der Gemeinde, dem PoP, bis zur Grundstücksgrenze des Kunden. Die korrekte Abbildung dieser hierarchischen Sterntopologie ist entscheidend für die Simulation der lokalen Verteilung.

Ziele:

Genaue Abbildung der lokalen Verteilungshierarchie: PoP -> NVt -> HÜP.

Modellierung der verschiedenen passiven Komponenten im Verteilnetz.

Inferenzbasierte Kartierung aller PoP-Standorte in Deutschland.

Betroffene Simulationskomponenten:

Datenbank (database.py): Erweiterung der Device-Typen.

Topologie-Engine (backend.py): Implementierung der hierarchischen Logik.

Geodaten-Verarbeitung (seed.py / backend.py): Skript zur Erstellung der PoP-Standorte.

Konkrete Umsetzungsschritte:

Detaillierte Modellierung der Netzkomponenten:

Beschreibung: Die lokale Verteilung besteht aus klar definierten passiven Komponenten, die als eigene Entitäten in der Simulation existieren müssen.

Umsetzung:

Point of Presence (PoP): Wird als zentraler, aktiver Knotenpunkt für jedes Ausbaugebiet modelliert. Er enthält die OLT-Hardware.

Optical Distribution Frame (ODF): Wird als passive Komponente innerhalb des PoP modelliert. Er ist der physische Startpunkt der Feeder-Kabel.

Netzverteiler (NVt) / Distribution Point (DP): Wird als neuer, passiver Gerätetyp eingeführt. Seine Funktion ist die Aufnahme von Spleißen und dem GPON-Splitter. Repräsentative Modelle (z.B. CCM NVt, Hexatronic) mit ihrer maximalen Spleißkapazität werden als auswählbare Templates hinterlegt.

Hausübergabepunkt (HÜP): Wird als neuer, passiver Gerätetyp modelliert. Er markiert den offiziellen Übergabepunkt vom öffentlichen Netz (NE3) in das Hausnetz (NE4).

Inferenzbasierte PoP-Kartierung:


Beschreibung: Da die exakten PoP-Adressen nicht öffentlich sind, wird eine plausible, modellbasierte Kartierung vorgenommen.

Umsetzung:

Ein Skript extrahiert alle in den Tabellen 6.1 bis 6.4 gelisteten Ausbaugebiete.

Für jede Gemeinde wird mithilfe eines Geokodierungsdienstes ein zentraler Punkt als angenommener PoP-Standort generiert. Der Genauigkeitsgrad wird als "Mittel (Inferiert)" gespeichert.

Diese tausenden von PoP-Knoten werden in der Datenbank gespeichert und auf der Karte visualisiert.

Visualisierung der PoP-zu-Backbone-Konnektivität:


Beschreibung: Die modellierten PoPs müssen plausibel an das nationale Backbone angebunden werden.

Umsetzung:

Ein Algorithmus im Backend verbindet jeden PoP-Knoten mit der geografisch nächstgelegenen Backbone-Trasse (GasLINE oder DB broadband).

Diese Verbindungen werden als "Regionale Anbindung" visualisiert und bilden die Brücke zwischen der nationalen und der lokalen Netzebene.

Erstellung einer DG-Referenz-Topologie (topology_dg_rees.yml):

Beschreibung: Um die Simulation greifbar zu machen, wird eine extrem detaillierte Referenz-Topologie für ein bekanntes Ausbaugebiet erstellt, z.B. für einen Ort im Kreis Kleve wie Rees.

Umsetzung:

Die Datei enthält: 1x PoP (modellierter Standort für Rees), mehrere NVt-Standorte, die plausibel in den Ortsteilen verteilt sind, und daran angeschlossene HÜPs für einzelne Adressen.

Die Links zwischen den Komponenten werden mit realistischen Längen (Feeder-Kabel, Verteilkabel) und den spezifischen Parametern aus den Dokumenten versehen.

Phase 3: Detaillierte physikalische PON-Schicht (Layer 1)
Diese Phase ist das Herzstück der physikalischen Simulation. Sie bildet die optischen Parameter und die Koexistenz der PON-Technologien mit höchster Präzision ab.

Ziele:

Exakte Berechnung des optischen Leistungsbudgets für jeden Kundenanschluss.

Simulation der Koexistenz von GPON und XGS-PON.

Detaillierte Abbildung aller Verlustfaktoren auf der "letzten Meile".

Betroffene Simulationskomponenten:

Datenbank (database.py): Detaillierte Properties für Devices und Links.

Simulations-Engine (backend.py): Überarbeitung der Berechnungslogik.

UI (main.js): Detaillierte Anzeige der physikalischen Werte.

Konkrete Umsetzungsschritte:

Detaillierte Datenmodelle für optische Parameter (database.py):

Beschreibung: Um eine präzise Berechnung zu ermöglichen, müssen alle relevanten Parameter in der Datenbank gespeichert werden können.

Umsetzung:

Device OLT: Properties werden erweitert um power_class ("B+" oder "C+"), transmit_power_dbm (z.B. "+5.0 dBm" für C+), supported_technologies (["GPON", "XGS-PON"]).

Device ONT: Properties werden erweitert um technology ("GPON" oder "XGS-PON") und sensitivity_min_dbm (z.B. "-30.0 dBm").

Device Splitter: Properties werden erweitert um split_ratio ("1:32") und insertion_loss_db (z.B. "-17.8 dB").

Link: Properties werden erweitert um length_km, attenuation_1310nm_db_km (0.35), attenuation_1490nm_db_km (ca. 0.35-0.4), attenuation_1577nm_db_km (ca. 0.25), connector_count (Anzahl der Stecker), splice_count (Anzahl der Spleiße).

Implementierung des Wellenlängenplans (backend.py):

Beschreibung: Die Simulation muss die unterschiedlichen Wellenlängen für GPON und XGS-PON berücksichtigen, um die Koexistenz korrekt abzubilden.

Umsetzung:

Die Funktion calculate_ont_power wird um einen Parameter technology erweitert.

Abhängig von der Technologie des ONTs wählt die Funktion die korrekte Wellenlänge für den Downstream (GPON: 1490nm, XGS-PON: 1577nm) und den entsprechenden Dämpfungswert des Links.

Präzise Berechnung des Leistungsbudgets (backend.py):

Beschreibung: Die Berechnungslogik wird überarbeitet, um alle im Bericht genannten Verlustfaktoren zu summieren.

Umsetzung:

total_loss = splitter_loss + (length * attenuation_per_km) + (connector_count * 0.5) + (splice_count * 0.1).

received_power_dbm = olt_transmit_power_dbm - total_loss.

Eine maintenance_margin von 3.0 dB wird ebenfalls einkalkuliert und vom verfügbaren Gesamtbudget abgezogen.

Erweiterte Alarm-Engine (backend.py):

Beschreibung: Die Alarme müssen die neuen, präzisen Parameter widerspiegeln.

Umsetzung:

"Signal Low" / "LOS": Wird ausgelöst, wenn received_power_dbm unter die sensitivity_min_dbm des ONTs fällt.

"Power Budget Exceeded": Wird ausgelöst, wenn total_loss größer ist als das durch die OLT-Klasse definierte Budget (28 dB für B+, 32 dB für C+).

"Technology Mismatch": Wird ausgelöst, wenn versucht wird, einen ONT mit einer Technologie an einem OLT-Port zu betreiben, der diese nicht unterstützt.

Visualisierung im Frontend (main.js):

Beschreibung: Der Nutzer muss alle physikalischen Details einsehen können.

Umsetzung:

Ein Klick auf einen ONT zeigt nicht nur den empfangenen Pegel an, sondern eine vollständige Aufschlüsselung des Leistungsbudgets: Sendeleistung OLT, abzüglich aller Verlustfaktoren, ergibt den finalen Empfangspegel.

Ein "Trace Path"-Tool visualisiert nicht nur den Pfad, sondern summiert entlang des Pfades alle Dämpfungswerte auf.

(Ende von Teil 1. Der nächste Teil wird die Phasen 4, 5 und 6 abdecken: PtP/AON-Architektur, Layer 2/3 Logik und die Dienstebene.)


 Quellen





Ok, weiter.



Gedankengang anzeigen
Verstanden. Hier ist der zweite Teil des ultra-detaillierten SPEC-Dokuments, der nahtlos an den ersten Teil anknüpft.

Phase 4: Aktive Ethernet-Architektur (PtP/AON)
Parallel zur passiven PON-Infrastruktur für Privatkunden betreibt die DG ein aktives Punkt-zu-Punkt (PtP) Netz für Geschäftskunden (DGB) und Premium-Privatkunden (DGH). Diese Phase widmet sich der vollständigen Simulation dieser zweiten Säule der hybriden DG-Architektur.

Ziele:

Simulation der dedizierten, ungeteilten Glasfaserverbindungen für Geschäftskunden.

Modellierung der spezifischen aktiven Hardwarekomponenten.

Abbildung der garantierten, symmetrischen Bandbreiten.

Betroffene Simulationskomponenten:

Datenbank (database.py): Neue Device-Typen und Link-Eigenschaften.

Simulations-Engine (backend.py): Eigene Berechnungs- und Logik-Pfade für AON.

UI/Frontend (main.js): Eindeutige Visualisierung der PtP-Architektur.

Konkrete Umsetzungsschritte:

Modellierung der PtP-Hardware:

Beschreibung: Für das AON-Netz wird spezifische Hardware im PoP und beim Kunden eingesetzt.

Umsetzung:

Neuer Device-Typ "AON Switch": Im PoP wird ein neuer Typ für aktive Switches eingeführt. Als Hardware-Template wird die Nokia 7360 ISAM Plattform mit den Leitungskarten NELT-B oder FELT-C hinterlegt. Jeder Port dieses Switches repräsentiert eine dedizierte Kundenverbindung.

Neuer Device-Typ "Business NT": Auf Kundenseite werden Netzabschlussgeräte wie der Nokia 7210 SAS-K oder der Cisco NCS 520 als auswählbare Modelle implementiert.

Einführung dedizierter PtP-Links:

Beschreibung: Im Gegensatz zu PON-Links, die an einem passiven Splitter enden, führen PtP-Links direkt zu einem aktiven Switch-Port.

Umsetzung:

Im Link-Modell wird ein neues Attribut link_technology mit den Werten "PON" und "PtP" eingeführt.

Ein "PtP"-Link kann nur zwischen einem "Business NT" und einem Port eines "AON Switch" bestehen.

Die calculate_ont_power-Funktion wird so angepasst, dass sie für PtP-Links keine Splitter-Dämpfung berechnet, was zu einem deutlich besseren Leistungsbudget führt.

Simulation von Service Level Agreements (SLAs):

Beschreibung: Ein Kernmerkmal von PtP ist die Bereitstellung garantierter, symmetrischer Bandbreiten.

Umsetzung:

"PtP"-Links erhalten eine Eigenschaft guaranteed_bandwidth_gbps.

Die Auslastungsberechnung (utilization_percent) wird für PtP-Links anders gehandhabt. Eine Überschreitung der garantierten Bandbreite löst einen spezifischen "SLA-Verletzung"-Alarm aus.

Visuelle Differenzierung im Frontend:

Beschreibung: Der Nutzer muss auf einen Blick die parallelen Architekturen unterscheiden können.

Umsetzung:

PtP-Links werden auf der Karte und in der Topologieansicht visuell hervorgehoben (z. B. durch eine dicke, violette Linie).

Ein neuer "Architektur"-Layer-Filter wird im UI eingeführt, der es erlaubt, nur das PON-Netz, nur das AON-Netz oder beide Netze gleichzeitig anzuzeigen.

Phase 5: Data Link & Network Layer (Layer 2/3)
Diese Phase ist entscheidend, da sie die spezifische und oft missverstandene Logik des Verbindungsaufbaus bei der DG emuliert. Die korrekte Nachbildung von DHCP, CGNAT und der IPv6-Präfixdelegation ist der Schlüssel zu einer aussagekräftigen Simulation.

Ziele:

Präzise Emulation des DHCP-basierten Verbindungsaufbaus ohne PPPoE.

Simulation der CGNAT-Implementierung für IPv4.

Detailgetreue Nachbildung der IPv6-Präfixdelegation (/56), inklusive des "Track Interface"-Mechanismus.

Aufklärung über den Mythos des VLAN-Taggings.

Betroffene Simulationskomponenten:

Simulations-Engine (backend.py): Implementierung der DHCP-, IPv4- und IPv6-Logik.

Router-Konfigurations-Emulator (Teil des backend.py oder ein neues Modul).

UI/Frontend (main.js): Anzeige der IP-Konfiguration und Fehlermeldungen.

Konkrete Umsetzungsschritte:

Emulation des DHCP-Verbindungsaufbaus:

Beschreibung: DG nutzt DHCP statt des bei anderen ISPs üblichen PPPoE. Der NT agiert als Vertrauensanker; die Authentifizierung erfolgt implizit über den provisionierten NT, oft gekoppelt an die MAC-Adresse des Kundenrouters.

Umsetzung:

Es wird ein virtueller DHCP-Server im Backend implementiert.

Ein simulierter Kundenrouter sendet einen DHCP-Discover.

Der Server antwortet nur, wenn die MAC-Adresse des anfragenden Routers in der Datenbank für diesen NT hinterlegt ist.

Szenario "Router-Wechsel": Tauscht der Nutzer in der Simulation den Router (und damit die MAC), antwortet der DHCP-Server nicht mehr. Ein neuer CLI-Befehl release-dhcp-lease <NT-ID> muss ausgeführt werden (simuliert Anruf bei der Hotline), um die neue MAC zu akzeptieren.

Simulation von "Kein VLAN-Tagging":

Beschreibung: Ein häufiger Konfigurationsfehler ist das Setzen eines VLAN-Tags am WAN-Port, was bei der DG (anders als bei der Telekom mit VLAN 7) falsch ist.

Umsetzung:

Der virtuelle Kundenrouter erhält eine Konfigurationsoption "WAN VLAN Tag".

Ist diese Option auf einen beliebigen Wert gesetzt, verwirft der simulierte NT die ankommenden DHCP-Pakete. Die UI zeigt den Fehler "Verbindung fehlgeschlagen: Unerwartetes VLAN-Tag am WAN-Port" an.

Implementierung von Carrier-Grade NAT (CGNAT) für IPv4:

Beschreibung: Privatkunden erhalten keine öffentliche IPv4-Adresse, sondern eine aus dem Bereich 100.64.0.0/10.

Umsetzung:

Der virtuelle DHCP-Server (siehe Schritt 1) vergibt IPv4-Adressen ausschließlich aus diesem Pool.

Eine simulierte "Internet"-Umgebung wird implementiert. Versucht ein Gerät aus dem Kunden-LAN eine Verbindung zu einem externen IPv4-Server aufzubauen, wird die private Quell-IP durch eine einzige, geteilte öffentliche IP des simulierten CGNAT-Routers ersetzt.

Szenario "Port-Weiterleitung schlägt fehl": Versucht der Nutzer eine Port-Weiterleitung für IPv4 einzurichten, zeigt die UI eine Warnung: "Eingehende Verbindungen über IPv4 sind aufgrund von Carrier-Grade NAT nicht möglich."

Emulation der DHCPv6 Prefix Delegation (/56):

Beschreibung: Dies ist der kritischste Teil. Der Kunde erhält ein ganzes /56-Präfix, was ihm 256 /64-Subnetze für sein internes Netzwerk ermöglicht. Ein häufiger Fehler ist die Anforderung eines /64-Präfixes, was Subnetting unmöglich macht.

Umsetzung:

Der virtuelle DHCPv6-Server im Backend wird so konfiguriert, dass er auf ein "DHCPv6 Solicit" mit Prefix-Delegation antwortet.

Die Konfiguration des simulierten Kundenrouters enthält die Option "Prefix Delegation Size".

Szenario "Korrekte Konfiguration": Fordert der Router "56" an, erhält er ein Präfix (z. B. 2a00:6020:abcd:ef00::/56). Die UI zeigt dann die verfügbaren 256 Subnetze (ef00 bis efff) an, die der Nutzer per "Track Interface" auf seine VLANs verteilen kann.

Szenario "Falsche Konfiguration": Fordert der Router "64" an, erhält er nur ein einziges /64-Präfix. Versucht er dann, ein weiteres VLAN mit "Track Interface" zu konfigurieren, erscheint die Fehlermeldung "Subnetting nicht möglich: Es wurde nur ein /64-Präfix vom ISP erhalten."

Phase 6: Service- & Applikationsebene (Layer 7)
Nachdem die Konnektivität hergestellt ist, widmet sich diese Phase der Simulation der darauf aufbauenden Dienste wie Telefonie und TV.

Ziele:

Emulation der SIP-basierten VoIP-Telefonie mit ihren spezifischen Anforderungen.

Simulation des modernen, OTT-basierten IPTV-Ansatzes.

Abbildung von Workarounds für CGNAT-Beschränkungen.

Betroffene Simulationskomponenten:

Simulations-Engine (backend.py): Logik für SIP-Registrierung und OTT-Verkehr.

Virtuelle Endgeräte (neues Modul): Emulation eines IP-Telefons oder einer TV-App.

UI/Frontend (main.js): Statusanzeige für Dienste.

Konkrete Umsetzungsschritte:

Emulation von VoIP (SIP):

Beschreibung: DG nutzt Standard-SIP. Die Registrierung erfordert spezifische Parameter und hängt oft von der Nutzung der DG-eigenen DNS-Server ab.

Umsetzung:

Ein virtueller SIP-Registrar wird im Backend unter der Adresse dg.voip.dg-w.de implementiert.

Ein emuliertes IP-Telefon im UI versucht, sich mit Benutzername und Passwort zu registrieren.

Szenario "DNS-Problem": Ist im simulierten Kundenrouter ein externer DNS-Server (z. B. 8.8.8.8) konfiguriert, schlägt die Namensauflösung für dg.voip.dg-w.de fehl. Das UI-Telefon zeigt den Fehler "Registrar nicht erreichbar". Wechselt der Nutzer auf "Vom ISP zugewiesene DNS-Server verwenden", funktioniert die Registrierung.

NAT-Problematik: Es wird ein "Static Port" Outbound-NAT-Szenario implementiert, um zu zeigen, wie dies die Stabilität der SIP-Verbindung verbessert.

Simulation von IPTV (Over-The-Top):

Beschreibung: Das TV-Angebot wird über den Partner waipu.tv als normaler Internet-Stream (OTT) realisiert. Es bedarf keiner speziellen Netzwerkkonfiguration wie VLANs oder IGMP-Proxies.

Umsetzung:

Eine simulierte "waipu.tv-App" wird als Endgerät im Kunden-LAN platziert.

Startet der Nutzer die App, generiert diese regulären HTTPS-Traffic an einen simulierten waipu.tv-Server im "Internet".

Lernziel: Die Simulation demonstriert, dass keine der für traditionelles IPTV typischen Konfigurationen (VLAN 8, IGMP) notwendig ist. Versucht der Nutzer diese dennoch zu konfigurieren, hat dies keinen Effekt, was die Einfachheit des OTT-Ansatzes verdeutlicht.

Abbildung von CGNAT-Workarounds:

Beschreibung: Es werden die im Dokument beschriebenen Methoden zur Umgehung von CGNAT simuliert.

Umsetzung:

Szenario "IPv6-Zugriff": Der Nutzer konfiguriert eine Firewall-Regel, um Port 443 zu einem internen Webserver (IPv6-Adresse) zu erlauben. Der Zugriff von einem externen IPv6-Client funktioniert.

Szenario "Reverse Tunnel": Es wird ein virtueller VPS im "Internet" platziert. Ein Gerät im LAN baut einen Tunnel zum VPS auf. Eingehende Anfragen an den VPS werden durch den Tunnel zum LAN-Gerät geleitet. Dies demonstriert die Machbarkeit, aber auch die Komplexität dieses Workarounds.

(Ende von Teil 2. Der nächste und letzte Teil wird die Phasen 7, 8 und 9 abdecken: Management-Protokolle, erweiterte Fehler-Szenarien und das UI/UX-Redesign.)






weiter



Gedankengang anzeigen
Verstanden. Hier ist der dritte und letzte Teil des SPEC-Dokuments. Dieser Teil konzentriert sich auf die betrieblichen Aspekte, die Emulation komplexer Fehlerszenarien und das finale User-Interface-Design, um alle simulierten Ebenen zugänglich zu machen.

Phase 7: Management-Protokolle und Betrieb
Diese Phase widmet sich der Simulation der betrieblichen Prozesse, die für die Provisionierung und Verwaltung der Endkundengeräte (ONTs) im DG-Netzwerk entscheidend sind.

Ziele:

Simulation des OMCI-Protokolls für die Fernverwaltung der ONTs.

Abbildung des impliziten, MAC-basierten Authentifizierungsmechanismus.

Verständnis der Rolle des NTs als "Vertrauensanker" des Netzes.

Betroffene Simulationskomponenten:

Simulations-Engine (backend.py): Implementierung der Management- und Authentifizierungslogik.

Datenbank (database.py): Speicherung von Provisionierungsstatus und MAC-Adressen.

UI/Frontend (main.js): Visualisierung des Gerätestatus und der MAC-Bindung.

Konkrete Umsetzungsschritte:

Emulation des OMCI-Protokolls (ONU Management and Control Interface):

Beschreibung: Die ONTs beim Kunden werden zentral vom Managementsystem der DG über das OMCI-Protokoll verwaltet. Dies ermöglicht die Fernkonfiguration und Fehlerdiagnose.

Umsetzung:

Ein Device vom Typ "ONT" erhält ein neues Attribut omci_status mit möglichen Werten wie unprovisioned, syncing, online, firmware_update.

Ein neuer CLI-Befehl activate-ont <ONT-ID> wird implementiert. Dieser simuliert den administrativen Akt der Provisionierung im DG-System.

Nach Ausführung des Befehls durchläuft der ONT in der UI sichtbar die Statusübergänge von unprovisioned über syncing zu online. Erst im Status online leitet der NT Datenverkehr an seinen Ethernet-Port weiter.

Simulation der MAC-Adressen-Bindung:

Beschreibung: Die Autorisierung des Anschlusses erfolgt implizit über den provisionierten NT und ist in der Praxis oft an die MAC-Adresse des am NT angeschlossenen Routers gekoppelt. Ein Wechsel des Routers (und damit der MAC) führt zu einem Konnektivitätsverlust, bis die serverseitige DHCP-Lease ausläuft oder zurückgesetzt wird.

Umsetzung:

Jeder ONT (bzw. dessen Port) in der Datenbank bekommt ein Feld bound_mac_address.

Wenn der simulierte DHCP-Server einen DHCP-Discover empfängt, prüft er, ob das bound_mac_address-Feld leer ist.

Wenn ja, wird die Quell-MAC des Pakets in das Feld eingetragen und eine IP-Adresse vergeben.

Wenn nein, wird die Quell-MAC des Pakets mit der bound_mac_address verglichen. Nur bei Übereinstimmung wird eine IP-Adresse vergeben.

Interaktives Szenario: Der Nutzer kann im UI den "Kundenrouter" durch einen Klick austauschen. Der neue Router hat eine andere MAC-Adresse. Die Simulation zeigt, dass dieser keine IP-Adresse mehr erhält. Die UI bietet dann eine Schaltfläche "DHCP-Lease zurücksetzen (DG Support anrufen)", die das bound_mac_address-Feld leert und die Verbindung für die neue MAC ermöglicht.

Phase 8: Erweiterte Szenarien und Fehler-Emulation
Diese Phase ist der Höhepunkt der Simulation. Sie bündelt das gesamte Wissen aus den vorherigen Phasen und ermöglicht es dem Nutzer, gezielt häufige Konfigurationsfehler und physikalische Probleme zu emulieren, um deren Auswirkungen live zu verstehen. Die Szenarien basieren direkt auf der "Checkliste zur Fehlervermeidung".

Ziele:

Schaffung einer interaktiven Lernumgebung zur Fehlerdiagnose.

Demonstration der Konsequenzen von Fehlkonfigurationen.

Simulation von physikalischen Störungen auf der "letzten Meile".

Betroffene Simulationskomponenten:

Szenario-Engine (neues Modul im backend.py).

Interaktive UI-Elemente (main.js).

Konkrete Umsetzungsschritte:

Implementierung von Layer-2/3-Fehlkonfigurationen:

Szenario "Falscher Verbindungstyp": Der Nutzer konfiguriert im simulierten Router "PPPoE" statt "DHCP". Die UI zeigt sofort eine Fehlermeldung "Authentifizierung fehlgeschlagen: DG verwendet kein PPPoE".

Szenario "Falsches VLAN-Tag": Der Nutzer konfiguriert am WAN-Port "VLAN ID 7". Die Simulation zeigt, dass keine DHCP-Anfragen den ISP erreichen. Fehlermeldung: "Keine Antwort vom Server: Unerwartetes VLAN-Tag am WAN-Port".

Szenario "Falsche Prefix-Größe": Der Nutzer fordert im DHCPv6-Client ein /64-Präfix an. Die WAN-Verbindung wird zwar hergestellt, aber beim Versuch, ein zweites internes VLAN mit "Track Interface" zu erstellen, erscheint die Fehlermeldung: "Subnetting fehlgeschlagen. Ursache: Es muss ein /56-Präfix vom ISP angefordert werden".

Implementierung von Service-Fehlkonfigurationen:

Szenario "VoIP-DNS-Problem": Der Nutzer konfiguriert im Router einen externen DNS-Server (z.B. Google). Die Internetverbindung funktioniert, aber das simulierte VoIP-Telefon zeigt den Fehler "SIP-Registrierung fehlgeschlagen: Registrar dg.voip.dg-w.de konnte nicht aufgelöst werden".

Simulation von physikalischen Störungen:

Szenario "Dreckiger Stecker / Hohe Dämpfung": Der Nutzer kann per Rechtsklick auf einen Link oder eine Komponente (z.B. HÜP, GF-TA) die Option "Störung simulieren -> Steckerdämpfung erhöhen" auswählen. Der connector_loss für diese Komponente wird auf einen hohen Wert (z.B. 5 dB) gesetzt. Die Simulation berechnet sofort den neuen, schlechteren Empfangspegel am ONT und löst ggf. einen "Signal Low"-Alarm aus.

Szenario "Rogue ONT": Ein erweiterter Modus, in dem der Nutzer einen ONT als "Rogue" markieren kann. Dieser simuliert ein dauerhaftes Senden im Upstream-Zeitschlitz. Die UI zeigt daraufhin, wie alle anderen ONTs am selben Splitter ihre Verbindung verlieren und offline gehen, während der Rogue-ONT selbst als Störungsquelle markiert wird.

Phase 9: UI/UX-Redesign und Gesamterlebnis
Die letzte Phase stellt sicher, dass die immense Komplexität und Detailtiefe der Simulation für den Nutzer zugänglich, verständlich und steuerbar ist.

Ziele:

Schaffung einer intuitiven und informativen Benutzeroberfläche.

Klare Visualisierung aller simulierten Ebenen und Parameter.

Einrichtung eines geführten "Lern-Modus" für Einsteiger.

Betroffene Simulationskomponenten:

Gesamtes Frontend (index.html, style.css, main.js).

Konkrete Umsetzungsschritte:

Entwicklung eines Multi-Layer-Dashboards:

Beschreibung: Die zentrale Karten- und Topologieansicht wird um schaltbare Layer erweitert, um die Informationsdichte zu steuern.

Umsetzung:

Geo-Layer: Zeigt die geografische Verteilung von Core Nodes, Backbone-Trassen und PoPs in Deutschland.

Physikalischer Layer: Visualisiert die optischen Parameter. Links werden entsprechend ihrer Dämpfung eingefärbt, ONTs zeigen ihren Empfangspegel an.

Technologie-Layer: Färbt Komponenten nach ihrer Technologie (GPON, XGS-PON, PtP) ein.

Service-Layer: Zeigt an, welche Dienste (Internet, VoIP) für einen Kunden aktiv sind und visualisiert den Datenverkehr.

Kontextsensitive Detail-Panels:

Beschreibung: Das "Eigenschaften"-Panel wird dynamisch und extrem detailliert.

Umsetzung:

Klick auf einen ONT: Zeigt nicht nur den Empfangspegel, sondern eine vollständige Aufschlüsselung des Power Budgets (OLT-Sendeleistung - Verluste = Empfangspegel), den omci_status und die provisionierten Dienste.

Klick auf einen PoP: Zeigt die installierte OLT-Hardware, die Anzahl der angeschlossenen Kunden und die Auslastung der Backbone-Anbindung.

Klick auf einen Kundenrouter: Zeigt die vollständige IP-Konfiguration (CGNAT-IPv4, öffentliches IPv6-Präfix), die MAC-Adresse und ermöglicht die Konfiguration von WAN, VLANs und Firewall-Regeln direkt im Panel.

Einführung eines geführten "Szenario-Modus":

Beschreibung: Um Einsteigern die Komplexität näherzubringen, wird ein geführter Modus entwickelt.

Umsetzung:

Der Nutzer kann ein Szenario aus einer Liste auswählen (z.B. "Eigenen Router erstmalig einrichten").

Die UI führt den Nutzer schrittweise durch die notwendige Konfiguration (WAN auf DHCP setzen, /56-Präfix anfordern etc.).

Bei jedem Schritt gibt die Simulation unmittelbares Feedback. Macht der Nutzer einen Fehler (z.B. VLAN-Tag setzen), erklärt ein Pop-up, warum dies falsch ist und wie die korrekte Einstellung lautet.

Dieser Modus verwandelt die Simulation von einem reinen Sandkasten in ein interaktives Tutorial für die DG-Netzwerktechnik.