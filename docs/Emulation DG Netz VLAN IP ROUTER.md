Emulation eines Deutsche Glasfaser (DG) FTTH-Anschlusses: Ein Technischer Leitfaden für VLANs, IP-Adressierung und Router-Konfiguration
Einleitung
Zweck und Zielgruppe
Dieser Bericht dient als maßgeblicher technischer Leitfaden für die Emulation eines modernen Deutsche Glasfaser (DG) FTTH-Anschlusses. Er richtet sich an Netzwerk-Profis, technisch versierte "Prosumer" und Systemadministratoren, die die Absicht haben, den vom Anbieter gestellten Router durch eigene, leistungsfähigere Hardware wie dedizierte Firewalls oder fortschrittliche Router zu ersetzen. Das Ziel ist es, ein tiefgreifendes, praxisorientiertes Verständnis der DG-Netzwerkarchitektur zu vermitteln und eine präzise, wiederholbare Laborumgebung für Tests, Konfigurationsvalidierung und Fehlerbehebung zu schaffen. Angesichts der spezifischen technischen Implementierung von Deutsche Glasfaser, die sich signifikant von traditionellen DSL- oder anderen Glasfaseranbietern in Deutschland unterscheidet, ist eine genaue Kenntnis der zugrundeliegenden Protokolle und Konfigurationsparameter unerlässlich für einen erfolgreichen Betrieb.

Abgrenzung: Emulation vs. Simulation
Im Kontext der Netzwerktechnik ist es entscheidend, zwischen Simulation und Emulation zu unterscheiden. Dieser Leitfaden konzentriert sich ausschließlich auf die Emulation.

Simulation: Werkzeuge wie Cisco Packet Tracer bilden das Verhalten von Netzwerkgeräten und Protokollen softwareseitig nach. Sie implementieren jedoch oft nur eine begrenzte Teilmenge der Befehle und Funktionen und können bei komplexen oder neueren Protokollen ungenau oder fehlerhaft sein. Insbesondere bei fortgeschrittenen IPv6-Funktionen wie der DHCPv6 Prefix Delegation (PD) stößt die Simulation schnell an ihre Grenzen.   

Emulation: Werkzeuge wie EVE-NG oder GNS3 schaffen eine virtualisierte Umgebung, in der reale Netzwerk-Betriebssysteme (NOS) – wie Cisco IOS, pfSense, OPNsense oder OpenWrt – unverändert ausgeführt werden. Dies ermöglicht es, die exakten Interaktionen zwischen dem Router des Kunden und dem Netzwerk des Internet Service Providers (ISP) mit höchster Detailtreue nachzubilden. Nur durch Emulation kann eine Konfiguration zuverlässig validiert werden, bevor sie in einer produktiven Umgebung zum Einsatz kommt.   

Für die präzise Nachbildung eines DG-Anschlusses, dessen Funktionalität maßgeblich von der korrekten Implementierung von DHCPv6-PD abhängt, ist die Emulation daher die einzig zielführende Methode.

Abschnitt 1: Dekonstruktion der Deutsche Glasfaser Netzwerkarchitektur
Um einen eigenen Router erfolgreich am DG-Anschluss zu betreiben, ist ein fundiertes Verständnis der spezifischen Netzwerkarchitektur des Anbieters unabdingbar. Diese Architektur weicht in wesentlichen Punkten von der anderer großer deutscher ISPs ab, was häufig zu Konfigurationsfehlern führt.

1.1 Physische und logische Topologie: Vom PoP zum NT
Der Weg des Signals vom Kernnetz des Anbieters bis zum Endkunden durchläuft mehrere definierte Stationen. Jede dieser Komponenten hat eine spezifische Funktion im Gesamtgefüge des Netzes.

Point of Presence (PoP): Dies ist die lokale Hauptverteilerstation von Deutsche Glasfaser im Ausbaugebiet. Der PoP dient als Knotenpunkt, der das überregionale Backbone-Netz mit den einzelnen Glasfaserleitungen zu den Haushalten verbindet. Er ist der aktive Ursprung des FTTH-Netzes in einer Gemeinde.   

Hausübergabepunkt (HÜP): Der HÜP ist der passive Punkt, an dem das Glasfaserkabel von der Straße in das Gebäude eintritt. Er wird typischerweise im Keller oder einem Hausanschlussraum installiert und stellt die physische Schnittstelle zum Haus dar. Ab diesem Punkt beginnt die Verantwortung des Eigentümers für die weitere Verkabelung im Haus.   

Glasfaser-Teilnehmeranschluss (GF-TA): In vielen Fällen wird vom HÜP eine Inhouse-Glasfaserleitung zu einer passiven Anschlussdose in der Wohnung oder einem zentralen Nutzungsort verlegt. Diese Dose wird als GF-TA bezeichnet. DG begrenzt die standardmäßige Länge dieser Leitung zwischen HÜP und GF-TA auf 20 Meter in Einfamilienhäusern und 30 Meter in kleineren Mehrfamilienhäusern.   

Network Terminator (NT) / Glasfaser-Modem: Der NT ist das entscheidende aktive Gerät in der Kette. Er wird an den GF-TA (oder direkt an den HÜP) angeschlossen und wandelt das optische Lichtsignal der Glasfaser in ein elektrisches Ethernet-Signal um, das über einen RJ45-Port (typischerweise LAN1) ausgegeben wird. Der NT ist der    

Demarkationspunkt auf Layer 2 zwischen dem DG-Netz und dem privaten Kundennetzwerk. Der Router des Kunden wird direkt an diesen Ethernet-Port des NT angeschlossen.

Ein kritischer Aspekt, der oft missverstanden wird, ist die Rolle des NT. Es handelt sich nicht um einen simplen Medienkonverter. Der NT ist ein vom Anbieter provisioniertes und verwaltetes Gerät. Die Konfiguration des NT ist ausschließlich durch Deutsche Glasfaser möglich. Diese Tatsache ist der Schlüssel zum Verständnis des Authentifizierungsmechanismus. Da für den Internetzugang bei DG keine klassischen Zugangsdaten wie bei PPPoE benötigt werden , erfolgt die Autorisierung des Anschlusses implizit über den beim Anbieter registrierten und provisionierten NT. In der Praxis wird diese Autorisierung oft mit der MAC-Adresse des am NT angeschlossenen Routers gekoppelt. Wechselt der Kunde seinen Router, muss die serverseitige DHCP-Lease, die an die alte MAC-Adresse gebunden ist, erst auslaufen – ein Prozess, der mehrere Stunden dauern kann –, bevor der neue Router eine IP-Adresse erhält. Der NT fungiert somit als Vertrauensanker des Netzes, der die Notwendigkeit einer aktiven Authentifizierung durch den Kunden eliminiert und den Prozess vereinfacht, aber gleichzeitig eine Intransparenz bei der Fehlerdiagnose schafft.   

1.2 Der Mythos des VLAN-Taggings: Eine definitive Klärung
Eine der hartnäckigsten und häufigsten Fehlerquellen bei der Konfiguration eigener Router an einem DG-Anschluss ist die Frage nach der Notwendigkeit von VLAN-Tagging.

Die Faktenlage ist eindeutig: Für den reinen Internetzugang sowie die darauf basierenden Dienste wie VoIP und das moderne IPTV-Angebot ist bei aktuellen Anschlüssen der Deutschen Glasfaser kein kundenseitiges VLAN-Tagging am WAN-Port des Routers erforderlich. Die Verbindung wird vom NT als standardmäßiger, untagged Ethernet-Frame bereitgestellt. Der Router muss lediglich eine IP-Adresse via DHCP an seiner WAN-Schnittstelle anfordern.   

Die weit verbreitete Verwirrung und die zahlreichen Falschinformationen in Online-Foren und sogar in einigen Herstelleranleitungen  haben eine klare Ursache: die Übertragung von Erfahrungswerten von anderen großen deutschen ISPs. Insbesondere bei Anschlüssen der Deutschen Telekom ist die Verwendung von VLANs zwingend erforderlich, um die verschiedenen Dienste voneinander zu trennen. Dort wird typischerweise    

VLAN 7 für den Internet-Traffic (und VoIP) und VLAN 8 für IPTV verwendet. Da viele Reseller wie 1&1, O2 oder Vodafone die Infrastruktur der Telekom nutzen, gilt diese Anforderung auch für deren Anschlüsse auf Telekom-Leitungen.   

Anwender, die von einem solchen Anschluss zur Deutschen Glasfaser wechseln, oder Administratoren, die mit der Telekom-Welt vertraut sind, gehen fälschlicherweise davon aus, dass eine ähnliche Konfiguration auch bei DG notwendig sei. Dies ist ein klassischer Fall von kognitiver Verzerrung durch fehlerhafte Analogiebildung. Deutsche Glasfaser verfolgt jedoch eine modernere, flachere Netzwerkarchitektur, bei der die Service-Trennung nicht über Layer-2-VLANs am Kundenendpunkt erzwungen wird. Während es Hinweise gibt, dass bei sehr alten DG-Installationen regional abweichende Konfigurationen existiert haben könnten, ist für alle aktuellen und zukünftigen Bereitstellungen die untagged-Methode der verbindliche Standard.   

Die folgende Tabelle stellt die fundamentalen Unterschiede in der Anschlusstechnik gegenüber und dient als schnelle Referenz zur Vermeidung von Konfigurationsfehlern.

Tabelle 1: Vergleich der WAN-Parameter (DG vs. andere deutsche ISPs)

Anbieter

Verbindungstyp

Internet VLAN ID

VoIP VLAN ID

IPTV VLAN ID

Deutsche Glasfaser (aktuell)

DHCP / DHCPv6

Keine

Keine

Keine (OTT)

Deutsche Telekom

PPPoE

7

7

8

Vodafone (eigene Leitung)

PPPoE

132

232 (variiert)

N/A

O2 (eigene Leitung)

PPPoE

11

N/A

N/A

M-Net

PPPoE

40

N/A

N/A

NetCologne

PPPoE

10

20

N/A


In Google Sheets exportieren
1.3 Verbindungsaufbau: DHCP statt PPPoE
Im Einklang mit der modernen, vereinfachten Architektur verzichtet Deutsche Glasfaser auf das Point-to-Point Protocol over Ethernet (PPPoE), das bei vielen etablierten DSL- und auch einigen Glasfaseranbietern zur Authentifizierung und zum Aufbau von Internetsitzungen verwendet wird. Stattdessen setzt DG auf ein reines DHCP-basiertes Verfahren.   

Der Prozess des Verbindungsaufbaus ist denkbar einfach:

Der WAN-Port des Kundenrouters wird mit dem LAN1-Port des NT verbunden.

Der Router ist so konfiguriert, dass er an seinem WAN-Interface eine IPv4-Adresse via DHCP und eine IPv6-Konfiguration via DHCPv6 anfordert.

Der Router sendet einen DHCP-Discover- (IPv4) und einen DHCPv6-Solicit-Request (IPv6) in das Netz.

Die Server im DG-Netzwerk antworten direkt mit einem DHCP-Offer (IPv4) und einem DHCPv6-Advertise (IPv6), die die vollständige IP-Konfiguration enthalten.   

Für diesen Prozess sind keinerlei Benutzername oder Passwort erforderlich. Die Autorisierung des Anschlusses erfolgt, wie zuvor beschrieben, implizit über den provisionierten NT und die daran gebundene MAC-Adresse des Routers.   

Diese Vorgehensweise hat direkte Auswirkungen auf die gesetzlich verankerte Routerfreiheit. Während der Kunde berechtigt ist, einen eigenen Router zu verwenden, muss dieser Wechsel dem Anbieter mitgeteilt werden. Ein Anruf bei der Service-Hotline oder eine entsprechende Einstellung im Kundenportal löst eine Änderung der Provisionierung auf der Serverseite aus, damit die MAC-Adresse des neuen Geräts akzeptiert wird. Wird dieser Schritt versäumt, erhält der neue Router keine IP-Adresse, bis die alte DHCP-Lease abgelaufen ist.   

Die Architektur von DG priorisiert somit die Einfachheit für den Standardkunden auf Kosten der Transparenz für den technisch versierten Nutzer. Das Modell ähnelt stark dem von Kabelnetzbetreibern (DOCSIS), bei dem das Kabelmodem provisioniert wird und der dahinter geschaltete Router seine Konfiguration per DHCP erhält. Dieses Design ist für ein reines IP-Netzwerk effizienter und vermeidet den Protokoll-Overhead von PPPoE. Die "Magie" der automatischen Provisionierung bleibt für den Endnutzer jedoch eine Blackbox, was die Fehlersuche bei Problemen erschweren kann.

1.4 IPv4 in einer CGNAT-Welt
Ein fundamentales Merkmal aller Privatkundenanschlüsse von Deutsche Glasfaser ist der Einsatz von Carrier-Grade NAT (CGNAT). Dies ist eine direkte Folge der weltweiten Knappheit an IPv4-Adressen.   

Private IPv4-Adressen: Der Router des Kunden erhält vom DG-Netzwerk keine eindeutige, öffentliche IPv4-Adresse. Stattdessen wird ihm eine private IP-Adresse aus dem speziell für CGNAT reservierten Adressbereich 100.64.0.0/10 zugewiesen.   

Geteilte öffentliche IP: Mehrere Kunden teilen sich eine einzige öffentliche IPv4-Adresse auf der Seite des Providers. Der CGNAT-Router des ISPs fungiert als ein riesiger, zentraler NAT-Router für Tausende von Kunden.

Konsequenzen für den Nutzer: Die gravierendste Folge von CGNAT ist, dass eingehende Verbindungen aus dem Internet standardmäßig nicht möglich sind. Da der CGNAT-Router nicht weiß, an welchen der vielen Kunden hinter der geteilten IP-Adresse ein eingehendes Datenpaket adressiert ist, verwirft er es. Dies verhindert klassische Anwendungsfälle wie:

Das Hosten von eigenen Servern (Web, Mail, Gameserver).

Standard-Port-Weiterleitungen.

Der direkte Zugriff auf Geräte im Heimnetz (z.B. NAS, Überwachungskameras).

Bestimmte Peer-to-Peer-Anwendungen und einige VPN-Typen, die eine direkte Erreichbarkeit erfordern.   

Eine feste, öffentliche IPv4-Adresse, die dieses Problem umgehen würde, ist bei DG nur in den deutlich teureren Geschäftskundentarifen ("DG business") enthalten. Es existieren zwar Drittanbieterlösungen und Workarounds (siehe Abschnitt 4.3), diese sind jedoch mit zusätzlichen Kosten oder technischem Aufwand verbunden.   

Die Entscheidung für CGNAT ist für einen schnell wachsenden Anbieter wie DG eine wirtschaftliche Notwendigkeit. Gleichzeitig ist sie aber auch eine strategische Weichenstellung: Sie positioniert IPv6 als den primären, vollwertigen und zukunftssicheren Internet-Stack. IPv4 wird zu einem reinen Kompatibilitätsdienst für den Zugriff auf ältere Teile des Internets degradiert. Für den Power-User bedeutet dies eine grundlegende Umstellung seiner Denkweise: Das Netzwerk muss nach dem Prinzip "IPv6-first" entworfen und gesichert werden.

1.5 Natives IPv6 und die Macht der Prefix Delegation
Das Herzstück der modernen Konnektivität bei Deutsche Glasfaser ist die native und umfassende IPv6-Implementierung. Sie ist nicht nur ein Zusatz, sondern die primäre Methode für eine direkte und uneingeschränkte Erreichbarkeit im Internet.

DHCPv6 Prefix Delegation (PD): Der entscheidende Mechanismus, den DG verwendet, ist die DHCPv6 Prefix Delegation. Anstatt dem Kundenrouter nur eine einzige IPv6-Adresse für seine WAN-Schnittstelle zuzuweisen, delegiert der ISP einen ganzen Block von Adressen – ein sogenanntes Präfix. Dies gibt dem Kunden die Hoheit, sein eigenes Netzwerk in Subnetze zu unterteilen.   

Die magische Zahl: /56: Die Größe des von DG delegierten Präfixes ist der kritischste Konfigurationsparameter für jeden Nutzer mit einem eigenen Router. Bei DG handelt es sich durchgängig um ein /56-Präfix. Ein    

/56-Präfix ist 56 Bits lang. Da ein vollständiges IPv6-Subnetz (ein LAN-Segment) immer eine Länge von 64 Bits hat, verbleiben dem Kunden 64−56=8 Bits zur freien Verfügung. Mit diesen 8 Bits kann er 2 
8
 =256 unterschiedliche /64-Subnetze in seinem Heimnetzwerk erstellen. Dies ist mehr als ausreichend, um eine komplexe Netzwerksegmentierung mit Dutzenden von VLANs (z.B. für private Geräte, IoT, Gäste, Server etc.) zu realisieren.

Der häufigste Fehler: /64 anfordern: Viele Forenbeiträge und fehlgeschlagene Konfigurationen resultieren aus einem fundamentalen Missverständnis dieses Konzepts. Wenn ein Router (oder der Benutzer) fälschlicherweise nur ein /64-Präfix vom ISP anfordert, erhält er zwar eine IPv6-Verbindung, aber dieses Präfix kann nicht weiter unterteilt werden. Ein    

/64 ist die kleinste atomare Einheit für ein IPv6-LAN. Der Versuch, daraus weitere Subnetze für VLANs abzuleiten, ist technisch unmöglich und führt zwangsläufig zum Scheitern des Vorhabens. Das Verständnis des Unterschieds zwischen der Anforderung eines /56- und eines /64-Präfixes ist der Scheideweg zwischen einer erfolgreichen, segmentierten Netzwerkkonfiguration und anhaltender Frustration.

Verbindungsprozess: Der Router erhält seine IPv6-Konfiguration durch eine Kombination aus DHCPv6 (für das Präfix und DNS-Server) und Router Advertisements (RA), die den Default Gateway ankündigen. Es gibt zahlreiche Berichte über eine signifikante Verzögerung bei der Ankunft der RAs nach dem Verbindungsaufbau. Es kann bis zu 15 oder sogar 30 Minuten dauern, bis die IPv6-Konnektivität vollständig hergestellt ist, da DG die RAs anscheinend in festen Intervallen sendet, anstatt direkt auf Router Solicitations zu antworten. Dies erfordert Geduld bei der Ersteinrichtung oder bei einem Router-Neustart.   

Abschnitt 2: Aufbau der Emulationsumgebung
Um die spezifische Konfiguration eines DG-Anschlusses sicher und wiederholbar zu testen, ist der Aufbau einer Emulationsumgebung unerlässlich. Diese Umgebung bildet das Zusammenspiel zwischen dem ISP-Netzwerk und dem Kundenrouter nach.

2.1 Wahl des Werkzeugs: EVE-NG als moderner Standard
Die Wahl der richtigen Software ist entscheidend für den Erfolg der Emulation.

Warum Emulation? Wie in der Einleitung dargelegt, ist die Emulation mit realen Router-Images (z.B. Cisco IOSv, pfSense, OpenWrt) zwingend erforderlich. Nur so lassen sich die komplexen Interaktionen von DHCPv6-PD, Router Advertisements und der anschließenden Subnetz-Bildung mittels "Track Interface" korrekt nachbilden. Simulatoren wie Packet Tracer sind hierfür ungeeignet. Ihre Implementierungen von IPv6-Protokollen sind oft unvollständig oder fehlerhaft, was zu irreführenden Ergebnissen führen würde.   

Vergleich der Emulatoren:

GNS3: Lange Zeit der De-facto-Standard, ist GNS3 ein leistungsstarker, kostenloser Emulator, der sich gut für den Einstieg und für Labs mit älteren Cisco IOS-Images eignet. Seine Stärke liegt in der Flexibilität und der großen Community. Die rein GUI-basierte Verwaltung von Topologien kann bei komplexen Setups jedoch unübersichtlich werden, und die Einrichtung gilt als weniger intuitiv als bei modernen Alternativen.   

EVE-NG (Emulated Virtual Environment - Next Generation): Hat sich in den letzten Jahren als Goldstandard für professionelle Netzwerkingenieure und komplexe Multi-Vendor-Labs etabliert. EVE-NG bietet eine zentrale, webbasierte Verwaltungsoberfläche, die die Erstellung und das Management von Labs erheblich vereinfacht. Es ist auf Skalierbarkeit ausgelegt und unterstützt eine breite Palette von virtuellen Appliances. Die    

EVE-NG Community Edition ist kostenlos und für die in diesem Leitfaden beschriebene Emulation vollkommen ausreichend und die empfohlene Wahl.   

Für dieses Projekt wird daher EVE-NG Community Edition empfohlen. Es bietet eine stabile, professionelle und skalierbare Plattform, die den Anforderungen voll gerecht wird. Umfassende Anleitungen zur Installation von EVE-NG auf VMware Workstation/Player oder ESXi sind weithin verfügbar.   

2.2 Kernkomponenten der Emulation
Die emulierte Topologie wird aus drei grundlegenden Knoten bestehen, die in EVE-NG miteinander verbunden werden:

Knoten 1: ISP-Router (Simulation des DG-Netzes): Dieser Knoten repräsentiert das Gateway im Netzwerk von Deutsche Glasfaser, mit dem der Kundenrouter kommuniziert. Ein virtuelles Router-Image von Cisco (IOSv oder IOSvL2) ist hierfür die ideale Wahl. Cisco IOS bietet eine robuste, flexible und exzellent dokumentierte Implementierung der serverseitigen DHCPv4- und DHCPv6-PD-Funktionen, die zur Nachbildung des DG-Verhaltens benötigt werden.   

Knoten 2: Kunden-Router/Firewall: Dies ist der zentrale Knoten des Experiments, in dem das Zielgerät des Benutzers läuft. Für diesen Leitfaden werden wir primär die Konfiguration einer virtuellen pfSense- oder OPNsense-Appliance demonstrieren, da diese bei Power-Usern und in KMU-Umgebungen sehr beliebt sind. Die Prinzipien sind jedoch direkt auf andere Systeme wie OpenWrt oder Ubiquiti EdgeRouter übertragbar.

Knoten 3: Client-Maschine: Um die Konnektivität, die IP-Adressvergabe und die Firewall-Regeln in den finalen LAN- und VLAN-Segmenten zu testen, wird ein Endgerät benötigt. Ein leichtgewichtiger Linux-Desktop (z.B. eine Lubuntu-VM) ist hierfür gut geeignet, da er vollwertige Netzwerk-Tools bietet. Alternativ kann für einfache Ping-Tests auch ein integrierter VPCS-Knoten in EVE-NG verwendet werden.   

2.3 Emulation des DG-"Internets": Konfiguration des ISP-Routers
Die präzise Konfiguration des emulierten ISP-Routers ist der Grundpfeiler für ein aussagekräftiges Labor. Die Konfiguration muss die asymmetrische Natur des DG-Anschlusses exakt widerspiegeln: ein stark eingeschränktes IPv4 und ein voll funktionsfähiges IPv6. Die folgenden Konfigurations-Snippets für Cisco IOS dienen als Vorlage.

2.3.1 IPv4-Konfiguration (CGNAT-Simulation)
Der ISP-Router muss dem Kundenrouter eine IP-Adresse aus dem CGNAT-Adressbereich 100.64.0.0/10 zuweisen. Ein einfacher DHCP-Pool genügt hierfür.

Beispiel-Konfiguration für Cisco IOS:

Cisco CLI

! Erstellen eines DHCP-Pools für den CGNAT-Bereich
ip dhcp pool DG_CGNAT_POOL
 network 100.100.100.0 255.255.255.0
 default-router 100.100.100.1
 dns-server 8.8.8.8
!
! Konfiguration der Schnittstelle, die zum Kundenrouter zeigt
interface GigabitEthernet0/1
 ip address 100.100.100.1 255.255.255.0
 no shutdown
Diese Konfiguration stellt sicher, dass der Kundenrouter eine IP-Adresse wie z.B. 100.100.100.2 erhält, die eindeutig als CGNAT-Adresse identifizierbar ist und keine öffentliche Routbarkeit besitzt.   

2.3.2 IPv6-Konfiguration (DHCPv6-PD mit /56-Präfix)
Dies ist der komplexere, aber entscheidende Teil der ISP-Emulation. Der Router muss so konfiguriert werden, dass er auf Anfrage ein /56-Präfix delegiert.

Beispiel-Konfiguration für Cisco IOS (basierend auf den Prinzipien aus ):   

Cisco CLI

! IPv6-Routing global aktivieren
ipv6 unicast-routing
!
! Definition des lokalen Präfix-Pools, aus dem delegiert wird.
! DG_PREFIX_POOL ist der Name.
! 2A00:6020:DEAD::/40 ist der Gesamt-Pool des ISPs.
! "56" ist die Länge des Präfixes, das an jeden Kunden delegiert wird.
ipv6 local pool DG_PREFIX_POOL 2A00:6020:DEAD::/40 56
!
! Erstellen des DHCPv6-Pools
ipv6 dhcp pool DG_DHCPV6_POOL
! Verknüpfung mit dem lokalen Präfix-Pool
 prefix-delegation pool DG_PREFIX_POOL
! Bereitstellung von DNS-Servern für die Kunden
 dns-server 2001:4860:4860::8888
 dns-server 2001:4860:4860::8844
!
! Konfiguration der Schnittstelle, die zum Kundenrouter zeigt
interface GigabitEthernet0/1
! Eine statische IPv6-Adresse für die ISP-Seite der Verbindung
 ipv6 address 2A00:6020:BEEF::1/64
! Aktivierung des DHCPv6-Servers auf dieser Schnittstelle
 ipv6 dhcp server DG_DHCPV6_POOL
! Aktivierung von Router Advertisements, damit der Kunde einen Default Gateway findet
 ipv6 nd other-config-flag
 no shutdown
Diese Konfiguration stellt sicher, dass ein Kundenrouter, der korrekt ein Präfix anfordert, ein eindeutiges /56-Präfix aus dem Bereich 2A00:6020:DEAD::/40 zugewiesen bekommt (z.B. 2A00:6020:DEAD:0100::/56). Die other-config-flag in den Router Advertisements signalisiert dem Client, dass er weitere Informationen (wie DNS-Server) über DHCPv6 abrufen soll.

Eine exakte Nachbildung dieser ISP-seitigen Konfiguration ist die Voraussetzung dafür, dass die Tests auf dem Kundenrouter aussagekräftige und auf die Realität übertragbare Ergebnisse liefern.

Abschnitt 3: Router-Konfiguration und Netzwerksegmentierung im Detail (Beispiel: pfSense/OPNsense)
Nachdem die Emulationsumgebung steht, folgt die Konfiguration des kundeneigenen Routers. Als primäres Beispiel dienen pfSense und OPNsense, da ihre Konfigurationslogik sehr ähnlich ist und sie bei technisch versierten Anwendern weit verbreitet sind.

3.1 Konfiguration der WAN-Schnittstelle
Die WAN-Schnittstelle ist das Tor zum Internet und ihre korrekte Konfiguration ist der erste und wichtigste Schritt. Die Einstellungen reflektieren die "Anfragen", die der Router an das DG-Netzwerk stellt.

IPv4 Configuration Type: Dieser wird auf DHCP gesetzt. Es sind keine weiteren spezifischen Einstellungen wie Hostname oder erweiterte Optionen erforderlich. Der Router erhält seine CGNAT-IP-Adresse automatisch.   

IPv6 Configuration Type: Dieser wird auf DHCP6 gesetzt. Dies aktiviert den DHCPv6-Client auf der WAN-Schnittstelle.

DHCPv6 Client Configuration: Dieser Abschnitt ist der entscheidende Teil. Hier werden die Parameter für die IPv6-Anfrage an den ISP definiert.

Request only an IPv6 prefix: Diese Option sollte aktiviert werden. Die primäre Aufgabe des Routers ist es, ein routbares Präfix für das LAN zu erhalten. Deutsche Glasfaser stellt nicht in allen Fällen eine dedizierte, routbare IPv6-Adresse für die WAN-Schnittstelle selbst bereit (eine sogenannte IA_NA - Identity Association for Non-temporary Addresses). Die Priorität liegt auf dem Erhalt eines Präfixes (IA_PD - Identity Association for Prefix Delegation). Die Aktivierung dieser Option stellt sicher, dass der Router sich auf das Wesentliche konzentriert und auch dann ein Präfix erhält, wenn der ISP keine einzelne WAN-Adresse zuweist.   

DHCPv6 Prefix Delegation size: Hier muss zwingend der Wert 56 ausgewählt werden. Dies ist der kritischste Konfigurationsschritt, um die vollen 256 Subnetze von DG zu erhalten und eine flexible Netzwerksegmentierung zu ermöglichen. Die Auswahl von 64 würde, wie in Abschnitt 1.5 erläutert, das gesamte Vorhaben der VLAN-Segmentierung mit IPv6 unmöglich machen.   

Send IPv6 prefix hint: Diese Option sollte ebenfalls aktiviert werden. Sie signalisiert dem DHCPv6-Server des ISPs explizit, dass ein Präfix der oben angegebenen Größe (56) gewünscht wird. Dies erhöht die Wahrscheinlichkeit einer korrekten Zuweisung.   

Die WAN-Konfiguration ist somit keine passive Zuweisung, sondern eine aktive, präzise formulierte Anfrage an das DG-Netzwerk. Nur wenn die Anfrage korrekt ist – insbesondere die Anforderung eines /56-Präfixes – wird der Server die erwartete Antwort liefern und das Fundament für eine erfolgreiche weitere Konfiguration legen.

3.2 Implementierung von LAN und VLANs
Sobald die WAN-Schnittstelle das /56-Präfix erfolgreich vom ISP erhalten hat, kann dieses zur Adressierung der internen Netzwerke verwendet werden. Dies ermöglicht eine saubere Trennung von Netzwerksegmenten durch VLANs.

3.2.1 VLAN-Erstellung und Zuweisung
Der erste Schritt ist die Definition der virtuellen LANs. In der Weboberfläche von pfSense/OPNsense erfolgt dies typischerweise unter Interfaces > Assignments > VLANs.

Für jedes gewünschte Netzwerksegment wird ein neues VLAN mit einem eindeutigen Tag (einer Nummer zwischen 1 und 4094) erstellt. Zum Beispiel:

VLAN 10 für das Haupt-LAN (MAIN)

VLAN 20 für IoT-Geräte (IOT)

VLAN 30 für Gäste (GUEST)

Anschließend werden diese neu erstellten VLANs unter Interfaces > Assignments neuen logischen Interfaces (z.B. OPT1, OPT2, OPT3) zugewiesen. Diese Interfaces werden dann aktiviert und erhalten aussagekräftige Namen (z.B. MAIN, IOT, GUEST).

3.2.2 IPv6-Subnetting mit dem delegierten /56-Präfix
Dies ist der Kern der IPv6-LAN-Konfiguration und der Punkt, an dem die Mächtigkeit der Prefix Delegation zum Tragen kommt.

"Track Interface" konfigurieren: Für jedes neu erstellte VLAN-Interface (MAIN, IOT, GUEST etc.) wird in dessen Konfiguration der IPv6 Configuration Type auf Track Interface gesetzt. Diese Einstellung weist das Interface an, seine IPv6-Konfiguration nicht selbstständig anzufordern, sondern sie vom WAN-Interface abzuleiten.   

IPv6 Track Interface Settings:

Track IPv6 Interface: Als Quelle für das Tracking wird das WAN-Interface ausgewählt.

IPv6 Prefix ID: Dies ist der entscheidende Parameter für das Subnetting. Hier wird für jedes VLAN ein eindeutiger hexadezimaler Wert zwischen $0$ und $ff$ (dezimal 0-255) eingetragen. Dieser Wert fungiert als Index und wählt eines der 256 verfügbaren /64-Subnetze aus dem vom WAN-Interface erhaltenen /56-Präfix aus.

Beispiel:

Das MAIN-VLAN erhält die Prefix ID $0$.

Das IOT-VLAN erhält die Prefix ID $1$.

Das GUEST-VLAN erhält die Prefix ID $2$.

Ein SERVERS-VLAN könnte die Prefix ID $a$ (hexadezimal für 10) erhalten.   

Router Advertisements (RA) aktivieren: Damit die Endgeräte in den jeweiligen VLANs ihre IPv6-Adressen automatisch konfigurieren können (via SLAAC) und weitere Informationen erhalten, muss der Router Advertisement Dienst konfiguriert werden. Unter Services > DHCPv6 Server & RA wird für jedes VLAN-Interface der RA-Dienst aktiviert. Übliche Modi sind:

Assisted: Der Router sendet RAs, die es den Clients erlauben, ihre Adresse via SLAAC selbst zu generieren, signalisiert aber gleichzeitig, dass zusätzliche Informationen (wie DNS) über einen DHCPv6-Server verfügbar sind.

Managed: Der Router weist die Clients an, ihre komplette IPv6-Konfiguration (Adresse, Gateway, DNS) von einem DHCPv6-Server zu beziehen.

Für die meisten Heim- und KMU-Netzwerke ist Assisted eine gute und flexible Wahl.   

Die folgende Tabelle visualisiert, wie aus einem einzigen vom ISP delegierten Präfix ein strukturiertes internes Netzwerk entsteht.

Tabelle 2: Beispielhafter IPv6-Subnetzplan aus einem /56-Präfix
(Angenommenes delegiertes Präfix: 2a00:6020:abcd:ef00::/56)

VLAN Name

VLAN ID

IPv6 Prefix ID

Resultierendes /64 Subnetz

MAIN

10

$0$

$2a00:6020:abcd:ef00::/64$

IOT

20

$1$

$2a00:6020:abcd:ef01::/64$

GUEST

30

$2$

$2a00:6020:abcd:ef02::/64$

SERVERS

40

$a$ (hex)

$2a00:6020:abcd:ef0a::/64$


In Google Sheets exportieren
3.2.3 Firewall-Strategien in einer IPv6-Welt
Der Übergang zu IPv6 bringt einen fundamentalen Paradigmenwechsel in der Netzwerksicherheit mit sich. Mit IPv4 und NAT waren Geräte im LAN standardmäßig von außen nicht direkt erreichbar. Diese "Sicherheit durch Unerreichbarkeit" war ein impliziter, oft unbeabsichtigter Nebeneffekt der Adressübersetzung. Bei IPv6 erhält jedes Gerät eine global eindeutige, routbare Adresse (GUA). Damit ist jedes Gerät potenziell ein direktes Ziel aus dem Internet. Eine explizite und korrekt konfigurierte Firewall ist daher nicht mehr nur eine Empfehlung, sondern eine absolute Notwendigkeit.   

Grundprinzip: "Default Deny" (Standardmäßig blockieren): Die wichtigste Firewall-Regel ist die Standardregel für eingehenden Verkehr auf der WAN-Schnittstelle. Diese muss auf Block oder Drop für jeglichen nicht explizit erlaubten Traffic gesetzt sein. Moderne Firewalls wie pfSense und OPNsense implementieren dieses sichere Grundprinzip standardmäßig.   

Essenzielle "Allow"-Regeln (auf der WAN-Schnittstelle, Richtung "IN"):

Erlaube etablierte/verwandte Verbindungen: Dies ist die grundlegendste Regel. Sie erlaubt Antwortpakete für Verbindungen, die von innerhalb des eigenen Netzwerks initiiert wurden. Ohne diese Regel könnte kein Gerät im LAN eine Verbindung zum Internet aufbauen.   

Erlaube ICMPv6: Im Gegensatz zu IPv4, wo ICMP (Ping) oft als Sicherheitsrisiko angesehen und blockiert wurde, ist ICMPv6 für die grundlegende Funktionalität von IPv6 unerlässlich. Protokolle wie Neighbor Discovery (NDP), Path MTU Discovery (PMTUD) und Router Discovery basieren auf ICMPv6. Ein pauschales Blockieren von ICMPv6 führt unweigerlich zu Verbindungsproblemen. Es ist Best Practice, die notwendigen ICMPv6-Typen explizit zu erlauben und potenziell missbrauchbare Typen wie Echo-Request (Ping) gegebenenfalls mit einem Rate-Limit zu versehen, um Denial-of-Service-Angriffe zu mitigieren.   

Erlaube selektive eingehende Dienste: Wenn ein Server oder Dienst im LAN von außen erreichbar sein soll (z.B. ein Webserver auf Port 443 oder ein WireGuard-VPN-Server auf Port 51820), muss hierfür eine explizite Firewall-Regel erstellt werden. Diese Regel muss den Traffic für das spezifische Protokoll (TCP/UDP), den Ziel-Port und die exakte IPv6-Adresse des Ziel-Hosts im LAN erlauben.   

Firewall für Inter-VLAN-Routing: Die Firewall ist auch für die Durchsetzung der Sicherheitsrichtlinien zwischen den internen VLANs zuständig. Hier werden Regeln definiert, die den Datenverkehr zwischen den Segmenten steuern. Ein typisches Beispiel ist, dem IOT-VLAN den Zugriff auf das MAIN-VLAN zu verbieten, während dem MAIN-VLAN der Zugriff auf das IOT-VLAN erlaubt wird, um Geräte verwalten zu können.

Die Sicherheit eines IPv6-Netzwerks ist somit explizit und nicht mehr implizit. Der Administrator muss aktiv definieren, welcher Verkehr erlaubt ist. Dies erfordert ein Umdenken, bietet aber letztendlich eine transparentere und granularere Kontrolle über die Netzwerksicherheit als das veraltete NAT-Modell.

Abschnitt 4: Konfiguration von Diensten und weiterführende Themen
Neben dem reinen Internetzugang bietet Deutsche Glasfaser auch Telefonie- und TV-Dienste an. Die Konfiguration dieser Dienste auf einem eigenen Router erfordert spezifische Kenntnisse.

4.1 Voice over IP (VoIP) Konfiguration
Deutsche Glasfaser realisiert die Telefonie über das standardisierte Session Initiation Protocol (SIP), also Voice over IP. Für die Nutzung mit einem eigenen Router oder einer eigenen Telefonanlage stellt DG die notwendigen Zugangsdaten zur Verfügung, die typischerweise im Kundenportal einsehbar oder im Begrüßungsschreiben enthalten sind.   

4.1.1 SIP-Parameter
Die folgenden Parameter sind für die Konfiguration eines SIP-Clients (z.B. in einer FRITZ!Box, einem IP-Telefon oder einer Software-Telefonanlage) erforderlich:

Registrar / Domain / Proxy: Der zentrale Server, bei dem sich der SIP-Client registrieren muss, lautet in der Regel dg.voip.dg-w.de. In älteren Dokumenten oder bei Geschäftskundenanschlüssen können auch die FQDNs    

business.voip.inexio.net oder tel.voip.inexio.net auftauchen, was auf die zugrundeliegende technische Plattform des Partners Inexio hinweist. Für Privatkunden ist    

dg.voip.dg-w.de der korrekte Wert.

Authentifizierungs-ID (Authentication ID / Auth-Name): Dies ist ein spezifischer Benutzername für die SIP-Authentifizierung, der von DG vergeben wird und sich vom Anzeigenamen oder der Telefonnummer unterscheiden kann.   

Benutzername (User ID / SIP-Account): Hier wird die vollständige Telefonnummer inklusive der Ortsvorwahl (ohne führende Null bei der Landesvorwahl, aber mit der Null bei der Ortsvorwahl, z.B. 02861...) eingetragen.   

Passwort: Das spezifische SIP-Passwort, das von DG bereitgestellt wird.   

Die folgende Tabelle fasst die wesentlichen Parameter für eine schnelle und fehlerfreie Konfiguration zusammen.

Tabelle 3: Referenztabelle für die VoIP-Konfiguration bei Deutsche Glasfaser

Parameter

Wert

Quelle

Protokoll

SIP

   

Registrar / Domain / Proxy

dg.voip.dg-w.de

   

Authentifizierungs-ID

<SIP-Username aus Kundendaten>

   

Benutzername / User ID

<Telefonnummer mit Vorwahl>

   

Passwort

<SIP-Passwort aus Kundendaten>

   

Bevorzugtes Protokoll

IPv4 (da Registrar nur A-Record hat)

   

4.1.2 Netzwerk- und Firewall-Anforderungen
DNS-Abhängigkeit: Eine erfolgreiche SIP-Registrierung hängt oft von der korrekten DNS-Auflösung des Registrars ab. Es gibt starke Hinweise darauf, dass der Hostname dg.voip.dg-w.de nur über die DNS-Server von Deutsche Glasfaser korrekt aufgelöst werden kann oder dass die Registrierung aus Stabilitätsgründen nur funktioniert, wenn diese genutzt werden. Ping-Versuche auf diesen Hostnamen von externen Netzen schlagen oft fehl, was auf eine interne oder eingeschränkte Erreichbarkeit hindeutet. Für eine stabile VoIP-Funktion wird daher empfohlen, entweder den gesamten Router oder zumindest die VoIP-Geräte die von DG per DHCP zugewiesenen DNS-Server verwenden zu lassen.   

Kein dediziertes VLAN: Im Gegensatz zu älteren ISP-Architekturen benötigt der VoIP-Dienst bei DG kein separates VLAN für den Transport. Der SIP- und RTP-Verkehr wird als normaler Datenverkehr über die bestehende Internetverbindung abgewickelt. Einige fortgeschrittene Nutzer entscheiden sich dennoch, ihre VoIP-Geräte in ein separates VLAN zu isolieren. Dies geschieht jedoch nicht aus einer technischen Notwendigkeit heraus, sondern um Quality of Service (QoS) Regeln gezielter anwenden oder spezifische DNS-Einstellungen nur für diese Geräte erzwingen zu können.   

NAT und Firewall: Da VoIP hinter einem NAT-Router betrieben wird (insbesondere im CGNAT-Szenario), können Probleme bei der Signalisierung und dem Aufbau der Sprachverbindung (RTP-Stream) auftreten. Um dies zu vermeiden, ist es oft notwendig, für ausgehenden Verkehr vom VoIP-Gerät die Option "Static Port" im Outbound NAT zu aktivieren. Dies verhindert, dass der Router die Quell-Ports der Pakete ändert, was für SIP-Server verwirrend sein kann. Eingehende Verbindungen für SIP (typischerweise Port 5060 TCP/UDP) und den RTP-Medienstrom (ein größerer Bereich von UDP-Ports, z.B. 7078-7110) müssen gegebenenfalls in der Firewall explizit an das VoIP-Gerät weitergeleitet werden, obwohl dies bei einer korrekten Outbound-Konfiguration oft nicht nötig ist.   

4.2 Der moderne IPTV-Ansatz: Over-The-Top (waipu.tv)
Deutsche Glasfaser hat sein ursprüngliches, eigenes IPTV-Angebot (realisiert durch die Tochtergesellschaft BrightBlue) eingestellt und ist eine strategische Partnerschaft mit dem Streaming-Anbieter waipu.tv eingegangen. Diese Entscheidung hat die technischen Anforderungen für den TV-Empfang grundlegend verändert und massiv vereinfacht.   

Technologie: Over-The-Top (OTT): Waipu.tv ist ein reiner OTT-Dienst. Das bedeutet, der TV-Stream wird wie jeder andere Internet-Streaming-Dienst (z.B. Netflix, YouTube, Amazon Prime Video) über die normale Internetverbindung übertragen. Der Datenverkehr ist regulärer, verschlüsselter HTTPS-Traffic.   

Keine spezielle Netzwerkkonfiguration: Durch den Wechsel zu einem OTT-Modell entfallen sämtliche komplexen Netzwerkkonfigurationen, die bei traditionellen, betreibergeführten IPTV-Lösungen notwendig waren. Insbesondere sind folgende Konfigurationen nicht mehr erforderlich:

Kein dediziertes IPTV-VLAN: Es gibt kein separates VLAN mehr für den TV-Verkehr.   

Kein IGMP-Proxy/Snooping: Da die Übertragung via Unicast (HTTPS) und nicht via Multicast erfolgt, sind Konfigurationen für das Internet Group Management Protocol (IGMP) auf dem Router oder den Switches hinfällig.

Keine speziellen QoS-Regeln: Während eine ausreichende Bandbreite wichtig ist, ist keine spezielle Priorisierung des IPTV-Traffics auf dem Router mehr notwendig.

Anforderungen: Die einzigen Voraussetzungen für die Nutzung des TV-Angebots sind eine stabile Internetverbindung (waipu.tv empfiehlt mindestens 16 Mbit/s für HD-Streams) und ein kompatibles Endgerät. Dazu zählen der waipu.tv 4K Stick, Amazon Fire TV, Apple TV, Google Chromecast, die meisten modernen Smart-TVs mit entsprechender App sowie Webbrowser auf PCs und mobile Apps für Smartphones und Tablets.   

Die strategische Entscheidung von DG, das IPTV-Geschäft an einen spezialisierten OTT-Anbieter auszulagern, ist ein Segen für Kunden, die einen eigenen Router betreiben möchten. Sie eliminiert eine ganze Klasse potenzieller Konfigurationsprobleme und macht den DG-Anschluss zu einer reinen "Internet-Pipe", über die alle Dienste als voneinander unabhängige Applikationen laufen. Die Komplexität wird vom Kundennetzwerk in die Cloud-Infrastruktur des Dienstleisters verlagert.

4.3 Umgehung von CGNAT-Beschränkungen
Für Power-User, die trotz des von DG eingesetzten CGNAT auf IPv4-basierte Dienste in ihrem Heimnetzwerk von außen zugreifen müssen, gibt es etablierte, wenn auch mit Aufwand verbundene, Workarounds.

IPv6 als primäre Lösung: Die direkteste und technisch sauberste Lösung ist, wann immer möglich, auf IPv6 auszuweichen. Da jedes Gerät im DG-Netz eine eindeutige öffentliche IPv6-Adresse besitzt, können Dienste direkt über diese Adresse erreichbar gemacht werden. Dies umgeht das CGNAT-Problem vollständig. Die einzige Voraussetzung ist, dass der zugreifende Client ebenfalls über eine IPv6-Verbindung verfügt. Für Clients, die sich in reinen IPv4-Netzen befinden, können Dienste wie Tunnelbroker (z.B. von Hurricane Electric, he.net) eine Brücke schlagen, indem sie ihnen einen IPv6-Tunnel zur Verfügung stellen.   

VPN mit Port-Weiterleitung: Einige kommerzielle VPN-Anbieter bieten als kostenpflichtiges Add-on eine dedizierte (statische) öffentliche IP-Adresse sowie die Möglichkeit zur Port-Weiterleitung an. Der Nutzer konfiguriert seinen Router oder ein Endgerät so, dass der gesamte oder ausgewählte Traffic über den VPN-Anbieter getunnelt wird. Der VPN-Server fungiert dann als Gateway zur Außenwelt mit einer eindeutigen öffentlichen IP. Eingehende Anfragen auf den weitergeleiteten Ports werden vom VPN-Server durch den Tunnel an das Gerät im Heimnetz weitergereicht.   

Reverse-Tunnel über einen Virtual Private Server (VPS): Dies ist die flexibelste, aber auch technisch anspruchsvollste Methode. Sie erfordert die Anmietung eines kleinen, günstigen VPS bei einem Cloud-Anbieter, der eine öffentliche IPv4-Adresse bereitstellt.

Ein Gerät im Heimnetz (z.B. ein Raspberry Pi oder eine Docker-Instanz) baut eine persistente, ausgehende Tunnelverbindung (z.B. via SSH, WireGuard oder Tailscale) zum VPS auf.

Auf dem VPS wird ein Reverse-Proxy (wie Nginx) oder eine Firewall-Regel (iptables) konfiguriert.

Eingehende Anfragen an die öffentliche IP-Adresse des VPS auf einem bestimmten Port werden von diesem entgegengenommen und durch den bereits bestehenden Tunnel "rückwärts" zum entsprechenden Server im Heimnetz weitergeleitet.   

Diese Workarounds lösen das CGNAT-Problem, verlagern aber die Kosten und die Komplexität auf den Nutzer. DG externalisiert damit die Verantwortung für den Betrieb öffentlich erreichbarer IPv4-Dienste an den Endkunden. Dies ist ein klares Indiz für die Branchenentwicklung, dass solche Anwendungsfälle im Privatkundensegment nicht mehr zum Standard-Leistungsumfang gehören und stattdessen die Nutzung von nativem IPv6 oder kommerziellen Cloud-Diensten der präferierte Weg ist.

Zusammenfassung und Checkliste der häufigsten Fallstricke
Der Betrieb eines eigenen Routers am Deutsche Glasfaser Anschluss ist problemlos möglich, erfordert jedoch die Kenntnis der spezifischen technischen Parameter, die sich von anderen Anbietern unterscheiden. Eine erfolgreiche Konfiguration hängt von wenigen, aber entscheidenden Einstellungen ab.

Kernparameter im Überblick
Verbindungstyp: DHCP für IPv4 und DHCPv6 für IPv6. Es wird kein PPPoE verwendet.   

VLAN ID: Für den Internetzugang ist kein VLAN-Tagging am WAN-Port erforderlich. Die Verbindung wird untagged bereitgestellt.   

IPv4-Adressierung: Carrier-Grade NAT (CGNAT). Der Router erhält eine private IP-Adresse aus dem Bereich 100.64.0.0/10. Eingehende Verbindungen sind nicht möglich.   

IPv6-Adressierung: Native Anbindung via DHCPv6 Prefix Delegation. Es muss zwingend ein /56-Präfix angefordert werden, um Subnetting für VLANs zu ermöglichen.   

VoIP-Konfiguration: Standard-SIP. Der Registrar lautet dg.voip.dg-w.de. Für eine stabile Funktion wird die Verwendung der DG-eigenen DNS-Server empfohlen.   

IPTV-Konfiguration: Realisiert als Over-The-Top (OTT) Dienst über den Partner waipu.tv. Es ist keine spezielle Netzwerkkonfiguration (VLAN, IGMP) auf dem Router erforderlich.   

Checkliste zur Fehlervermeidung
Die folgende Checkliste fasst die häufigsten Fehler und Missverständnisse zusammen, die bei der Einrichtung eines eigenen Routers am DG-Anschluss auftreten:

❌ Falle 1: PPPoE konfigurieren.

Fehler: Der Router wird für eine PPPoE-Einwahl mit Benutzername und Passwort konfiguriert.

Korrektur: Der WAN-Port muss auf reines DHCP (für IPv4) und DHCPv6 (für IPv6) eingestellt sein. Es werden keine Zugangsdaten benötigt.   

❌ Falle 2: VLAN 7 taggen.

Fehler: Am WAN-Port wird ein VLAN-Tag mit der ID 7 konfiguriert.

Korrektur: Diese Einstellung ist für die Deutsche Telekom korrekt, nicht für Deutsche Glasfaser. Die WAN-Schnittstelle muss untagged betrieben werden.   

❌ Falle 3: Ein /64-IPv6-Präfix anfordern.

Fehler: In den DHCPv6-Client-Einstellungen wird eine Prefix Delegation Size von 64 angefordert.

Korrektur: Dies ist der kritischste Fehler, der eine Netzwerksegmentierung verhindert. Es muss immer eine Prefix Delegation Size von 56 angefordert werden, um die 256 Subnetze von DG zu erhalten.   

❌ Falle 4: Eigene DNS-Server für VoIP verwenden.

Fehler: Alternative DNS-Server (z.B. Google, Cloudflare) werden für das gesamte Netzwerk konfiguriert, einschließlich der VoIP-Geräte.

Korrektur: Die SIP-Registrierung bei dg.voip.dg-w.de kann fehlschlagen, wenn nicht die DNS-Server von DG verwendet werden. VoIP-Geräte sollten entweder direkt die DG-DNS-Server nutzen oder der Router muss sicherstellen, dass er Anfragen für die DG-Domain korrekt weiterleitet.   

❌ Falle 5: Router wechseln und sofortige Verbindung erwarten.

Fehler: Nach dem Austausch des Routers wird eine sofortige Internetverbindung erwartet.

Korrektur: Aufgrund der serverseitigen Bindung an die MAC-Adresse des Routers kann es mehrere Stunden dauern, bis der neue Router eine DHCP-Lease erhält. Dieser Prozess kann durch einen Anruf beim DG-Support, der die Provisionierung zurücksetzt, oder durch das Klonen der MAC-Adresse des alten Routers auf den neuen beschleunigt werden.   

Durch die Beachtung dieser zentralen Punkte und das Verständnis der zugrundeliegenden Architektur steht einem erfolgreichen und stabilen Betrieb eines leistungsfähigen, eigenen Routers am Glasfaseranschluss der Deutschen Glasfaser nichts im Wege.

