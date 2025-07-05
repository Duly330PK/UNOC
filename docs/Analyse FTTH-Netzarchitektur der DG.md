Analyse der FTTH-Netzarchitektur der Deutschen Glasfaser
Executive Summary
Dieser Bericht bietet eine detaillierte technische Analyse der Netzarchitektur der Deutschen Glasfaser (DG). Die Untersuchung zeigt, dass die DG eine hochentwickelte und strategisch ausgerichtete Infrastruktur betreibt, die speziell für den kosteneffizienten und skalierbaren Ausbau von Fiber-to-the-Home (FTTH) in ländlichen und suburbanen Regionen Deutschlands konzipiert ist. Die Kernstrategie basiert auf einer hybriden Architektur, die zwei primäre Technologien kombiniert: ein passives optisches Netz (PON) für den Massenmarkt der Privatkunden und ein aktives Punkt-zu-Punkt (PtP) Ethernet-Netz für Geschäftskunden mit höheren Leistungsanforderungen. Diese duale Strategie ermöglicht es der DG, die Investitionsrendite in jedem Ausbaugebiet zu maximieren.

Die Netzwerktopologie folgt einem klassischen hierarchischen Sternmodell, das an einem zentralen Point of Presence (PoP) beginnt und sich über passive Netzverteiler (NVt) bis zu den einzelnen Hausanschlüssen erstreckt. Technologisch setzt die DG auf etablierte Standards wie GPON, migriert aber seit 2024 strategisch auf das leistungsfähigere, symmetrische XGS-PON, um Multi-Gigabit-Dienste anbieten zu können. Ein durchdachter Wellenlängenplan stellt die Koexistenz beider Technologien auf derselben Faser sicher und macht die Infrastruktur zukunftssicher.

Die Analyse der konkreten technischen Parameter, einschließlich Splitter-Verhältnissen von typischerweise 1:32 und einem robusten optischen Leistungsbudget, verdeutlicht die ingenieurtechnische Präzision, die auf eine Maximierung der Reichweite bei gleichzeitiger Gewährleistung der Servicequalität abzielt. Gepaart mit modernen, minimalinvasiven Bauverfahren und einer standardisierten Inhouse-Installation bildet die Architektur der Deutschen Glasfaser ein ganzheitliches System, das auf schnelle, wiederholbare und wirtschaftlich tragfähige FTTH-Rollouts im großen Stil optimiert ist.

1.0 Strategische und architektonische Übersicht
1.1 Netzwerkphilosophie: Dominanz im ländlichen FTTH-Markt durch eine hybride Architektur
Die grundlegende Geschäfts- und Netzwerkstrategie der Deutschen Glasfaser ist klar definiert: die Erschließung des ländlichen und suburbanen Raums in Deutschland mit reinen Glasfaseranschlüssen bis in die Wohnung (Fiber-to-the-Home, FTTH). Diese Fokussierung unterscheidet das Unternehmen von etablierten Anbietern, die sich historisch auf dichter besiedelte städtische Gebiete konzentrierten. Das Geschäftsmodell der DG basiert auf dem Prinzip des "Open Access", was bedeutet, dass das Unternehmen die physische Infrastruktur plant, baut und betreibt und diese auch anderen Dienstanbietern zur Verfügung stellt, wie es beispielsweise durch ein umfassendes Wholesale-Abkommen mit Vodafone der Fall ist.   

Um dieses Ziel in Gebieten mit geringerer Bevölkerungsdichte wirtschaftlich tragfähig zu gestalten, hat die Deutsche Glasfaser eine hybride Netzwerkarchitektur implementiert. Diese Architektur stützt sich auf zwei technologische Säulen: Eine passive, geteilte Infrastruktur für den breiten Privatkundenmarkt und eine dedizierte, aktive Infrastruktur für Geschäftskunden mit höheren Anforderungen an Bandbreite und Servicequalität.   

1.2 Die zwei Säulen: Passives Optisches Netz (PON) und Punkt-zu-Punkt (PtP) Ethernet
Die Koexistenz zweier unterschiedlicher, aber komplementärer Technologien ist das Herzstück der Flexibilität und Wirtschaftlichkeit des DG-Netzes.

Passive Optical Network (PON): Dies ist die grundlegende Technologie für das Privatkundengeschäft der Deutschen Glasfaser. PON nutzt eine Punkt-zu-Mehrpunkt-Topologie (PtMP), bei der eine einzelne Glasfaser, die von einem zentralen Punkt ausgeht, über einen passiven optischen Splitter aufgeteilt wird, um mehrere Haushalte – in der Praxis typischerweise 32 – zu versorgen. Der entscheidende Vorteil dieser Architektur liegt in der Eliminierung aktiver, stromverbrauchender Komponenten im Verteilnetz zwischen der Vermittlungsstelle und dem Kunden. Dies reduziert die Betriebskosten (OPEX) durch geringeren Stromverbrauch, weniger Wartungsaufwand und keine Notwendigkeit für Klimatisierung in den Straßenverteilern erheblich, was den Ausbau in ländlichen Gebieten erst wirtschaftlich macht.   

Point-to-Point (PtP) Ethernet: Für Geschäftskunden (DGB-Dienste) und ausgewählte Premium-Privatkunden (DGH) bietet die Deutsche Glasfaser eine dedizierte Punkt-zu-Punkt-Verbindung, auch als Active Optical Network (AON) bekannt. Bei diesem Modell erhält jeder Kunde eine eigene, ungeteilte Glasfaser bis zu einem aktiven Switch-Port in der lokalen Vermittlungsstelle. Diese Architektur ermöglicht die Bereitstellung von symmetrischen, garantierten Bandbreiten und ist die Grundlage für die Erfüllung strenger Service Level Agreements (SLAs), wie sie im Geschäftskundenumfeld gefordert werden.   

Die Fähigkeit, beide Architekturen über dieselbe physische Backbone- und Leerrohrinfrastruktur zu betreiben, zeugt von einem pragmatischen und hochgradig optimierten Netzwerkdesign. Es erlaubt der DG, den Return on Investment (ROI) in jeder erschlossenen Gemeinde zu maximieren, indem sie die unterschiedlichen Bedürfnisse und Zahlungsbereitschaften von Privat- und Geschäftskunden mit der jeweils am besten geeigneten und kosteneffizientesten Technologie bedient.

1.3 Netzwerkevolution: Der Übergang zu "Central Offices" der nächsten Generation
Die Deutsche Glasfaser modernisiert nicht nur die Übertragungstechnologie selbst, sondern auch das grundlegende Design ihrer Netzwerkknotenpunkte. Ein Pilotprojekt in Vettelschoß demonstriert ein neues Konzept namens "Central Office", das die bisherigen Points of Presence (PoPs) ersetzen oder ergänzen soll.   

Diese neuen Technikzentralen sind signifikant kleiner und energieeffizienter. Sie sollen den Stromverbrauch pro Kunde auf ein Drittel im Vergleich zu konventionellen Glasfasernetzen senken, die ihrerseits bereits nur etwa 20 % des Energiebedarfs von Kupfernetzen haben. Erreicht wird dies unter anderem durch eine Konzentration der aktiven Technik und den Einsatz moderner, hitzebeständiger Hardwarekomponenten, die keine aufwendige Klimatisierung mehr benötigen.   

Durch diese Neugestaltung wird der Platzbedarf für technische Standorte pro Kunde um rund 90 % reduziert. Dies ermöglicht eine flexiblere Platzierung der Zentralen, beispielsweise am Ortsrand, was die Bauplanung vereinfacht, Anwohner weniger beeinträchtigt und den Ausbau gemäß der DIN-Norm 18220 für minimalinvasive Verlegeverfahren beschleunigt. Dieser Schritt ist eine logische Weiterentwicklung der Kostenoptimierungsstrategie der DG, die sowohl die Investitionskosten (CAPEX) durch kleinere Standorte und einfachere Bauprozesse als auch die Betriebskosten (OPEX) durch geringeren Energieverbrauch senkt.   

2.0 Makro-Level Netzwerktopologie: Vom Backbone zum lokalen Knotenpunkt
2.1 Nationale Backbone-Integration und Interkonnektion
Das Netzwerk der Deutschen Glasfaser beginnt nicht isoliert in den einzelnen Gemeinden, sondern ist an die großen nationalen und internationalen Internet-Backbones angebunden. Diese Anbindung erfolgt an wichtigen Internet-Austauschknoten (IXPs) und in Telekommunikationszentren (Telehäusern).   

Um die Reichweite effizient zu vergrößern und insbesondere die anvisierten ländlichen Gebiete zu erreichen, setzt die Deutsche Glasfaser auf strategische Partnerschaften. Ein zentraler Partner ist GasLINE, dessen über 25.000 km langes Glasfasernetz von der DG genutzt wird, um die eigenen regionalen Netze an das übergeordnete Kernnetz anzubinden. Diese Kooperation ist ein klassisches Beispiel für eine "Build vs. Buy"-Entscheidung: Statt selbst teure und zeitaufwendige Langstreckenverbindungen zu bauen, nutzt die DG vorhandene Infrastruktur und kann ihr Kapital und ihre Ressourcen auf den kritischsten und komplexesten Teil des Ausbaus konzentrieren – die sogenannte "letzte Meile" zum Kunden.   

2.2 Das lokale Verteilmodell: Eine hierarchische Sterntopologie
Auf lokaler Ebene, innerhalb einer Gemeinde oder eines Ausbaugebiets, wird das Netz nach einer hierarchischen Stern- oder Baum-und-Ast-Topologie aufgebaut. Diese Struktur ist nachweislich die effizienteste Methode, um ein Signal von einem zentralen Punkt zu einer großen Anzahl von Endpunkten zu verteilen. Die Hierarchie gliedert sich wie folgt:   

Netzebene 2/3 - Der Point of Presence (PoP): Dies ist der zentrale Knotenpunkt und das Herz des lokalen Netzes für eine ganze Gemeinde oder einen großen Stadtteil. Der PoP fungiert als Kopfstation (Head-End) und bildet die Schnittstelle zwischen dem Weitverkehrsnetz (Backbone) und dem lokalen Zugangsnetz (Access Network). Hier wird das Signal vom Backbone übernommen und für die lokale Verteilung aufbereitet.   

Netzebene 3 - Feeder-Kabel: Vom PoP aus werden hochkapazitive Feeder-Kabel (Zuführungskabel) sternförmig zu verschiedenen strategischen Punkten innerhalb des Ausbaugebiets verlegt. Diese Kabel bündeln eine große Anzahl von Fasern.   

Netzebene 3 - Der Distribution Point (DP) / Netzverteiler (NVt): An den Enden der Feeder-Kabel stehen die Straßenverteiler, die von der DG als Distribution Points (DP) oder im deutschen Branchenstandard als Netzverteiler (NVt) bezeichnet werden. In diesen passiven Schränken findet die eigentliche Aufteilung statt. Hier werden die Fasern aus dem dicken Feeder-Kabel auf eine Vielzahl von dünneren Verteilkabeln aufgeteilt, die dann die einzelnen Straßen versorgen.   

Netzebene 4 - Der Hausanschluss: Vom nächstgelegenen DP/NVt wird für jeden einzelnen Kunden eine dedizierte Glasfaser bis ins Haus oder die Wohnung verlegt. Dies unterstreicht das FTTH-Versprechen der DG, bei dem jeder Kunde eine eigene, ungeteilte Leitung ab dem letzten Verteilerpunkt erhält.   

2.3 Architekturbild 1: Schematische Darstellung der Netzwerkhierarchie
Das Gesamtbild der Netzarchitektur lässt sich als eine Kaskade von Verteilungspunkten visualisieren. An der Spitze steht die Anbindung an einen nationalen Internet-Austauschknoten (IXP). Von dort führt eine Verbindung über ein Partner-Backbone (z.B. GasLINE) zum lokalen Point of Presence (PoP) der Deutschen Glasfaser am Rande einer Gemeinde. Innerhalb des PoP wird das Signal aufbereitet und auf mehrere Feeder-Kabel verteilt, die sternförmig in die verschiedenen Ortsteile führen. Diese Feeder-Kabel enden in den passiven Netzverteilern (NVt/DP) an den Straßen. In diesen Verteilern wird das Signal erneut aufgeteilt und über individuelle Glasfasern zu den einzelnen Haushalten (Hausübergabepunkt, HÜP) geführt. Diese hierarchische Struktur minimiert die Gesamtlänge der benötigten Glasfaserkabel und die Anzahl der erforderlichen Ports im PoP, was eine grundlegende Voraussetzung für die Wirtschaftlichkeit des ländlichen Ausbaus ist.

3.0 Das Verteilnetz: Eine detaillierte Komponentenanalyse
3.1 Der Point of Presence (PoP): Das Herz des lokalen Netzes
3.1.1 Physische Merkmale und Funktion
Der PoP ist die zentrale technische Einrichtung für ein lokales Ausbaugebiet und bildet die entscheidende Schnittstelle zwischen dem überregionalen Backbone-Netz und dem Zugangsnetz, das die Kunden versorgt. Physisch handelt es sich dabei meist um ein vorgefertigtes, betoniertes Gebäude von der Größe einer Garage. Lieferanten wie R&M geben typische Außenmaße von beispielsweise    

2,5×4,5×3,5 Meter (Gewicht: 20,5 Tonnen) oder 2,5×6,0×3,5 Meter (Gewicht: 25,5 Tonnen) an. Als aktive Vermittlungsstelle beherbergt der PoP eine Vielzahl von technischen Komponenten und erfordert daher eine redundante Stromversorgung, eine präzise Klimatisierung zur Kühlung der aktiven Geräte sowie umfassende Sicherheitsmaßnahmen wie Zutrittskontrollsysteme. Die Deutsche Glasfaser setzt auf Fernüberwachung von Umgebungsparametern wie Temperatur und Luftfeuchtigkeit, um die Betriebssicherheit der Komponenten zu gewährleisten und die Wartungskosten zu optimieren.   

3.1.2 Aktive Technologie: Der Optical Line Terminal (OLT)
Das wichtigste aktive Element im PoP ist der Optical Line Terminal (OLT). Dieses Gerät ist der Motor des PON-Netzes. Es erzeugt die optischen Downstream-Signale für alle angeschlossenen Kunden und empfängt deren gebündelte Upstream-Signale. Für die Bereitstellung der PtP-Dienste für Geschäftskunden setzt die DG auf dedizierte Hardware, wie die Nokia 7360 ISAM-Plattform, die als Layer-2-Switch und Aggregator fungiert.   

Eine zentrale strategische Entscheidung war die im Mai 2024 bekannt gegebene Partnerschaft mit Nokia. Im Rahmen dieser Kooperation wird die nächste Generation von PON-Lösungen implementiert, die auf derselben Hardwareplattform GPON, XGS-PON und zukünftig sogar 25G-PON unterstützen kann. Dies sichert der Deutschen Glasfaser einen klaren und kosteneffizienten Migrationspfad zu höheren Bandbreiten, ohne die Kernhardware austauschen zu müssen.   

3.1.3 Passive Infrastruktur: Optical Distribution Frames (ODF)
Neben der aktiven Technik beherbergt der PoP auch die zentrale passive Verteilerinfrastruktur, den Optical Distribution Frame (ODF), auch als Glasfaser-Hauptverteiler bezeichnet. Dies ist ein Gestellsystem, in dem die ankommenden Fasern aus dem Backbone-Netz ankommen, gespleißt (dauerhaft verbunden) und auf die einzelnen Feeder-Kabel, die in das lokale Netz führen, aufgeteilt werden. Der ODF ist der physische Ausgangspunkt für die sternförmige Verteilung des Glasfasernetzes in der Gemeinde.   

3.2 Straßenverteilung: Netzverteiler (NVt) und Distribution Points (DP)
3.2.1 Funktion und Platzierung in der Netzwerkhierarchie
Der Netzverteiler (NVt) ist der moderne Fachbegriff für den früher als Kabelverzweiger (KVz) bekannten grauen Kasten am Straßenrand. Die Deutsche Glasfaser verwendet für diese Unterverteiler auch den Begriff Distribution Point (DP).   

Diese Schränke sind rein passive Komponenten der Netzinfrastruktur. Ihre einzige Funktion ist es, die ankommenden Fasern aus dem Feeder-Kabel aufzunehmen und über Spleißverbindungen oder durch passive optische Splitter auf die kleineren Verteilkabel zu verteilen, die zu den einzelnen Grundstücken führen. Sie enthalten keinerlei aktive, stromverbrauchende Elektronik, was ein Kernprinzip des kosteneffizienten PON-Designs ist. Die Gehäuse bestehen aus robusten Materialien wie glasfaserverstärktem Polycarbonat oder pulverbeschichtetem Aluminium und sind nach Schutzklassen wie IP54 oder IP55 zertifiziert, um die empfindlichen Glasfaserverbindungen im Inneren vor Wasser, Staub und Vandalismus zu schützen.   

3.2.2 Tabelle: Vergleich repräsentativer Netzverteiler-Modelle
Die im Feld eingesetzten Netzverteiler sind modular und skalierbar, um den unterschiedlichen Anforderungen – von einem kleinen Wohngebiet bis hin zu einem dicht besiedelten Stadtteil – gerecht zu werden. Die folgende Tabelle fasst die Spezifikationen typischer Modelle von Zulieferern zusammen, die repräsentativ für die im Markt verwendeten Komponenten sind.

Modellserie (Beispiel)

Max. Spleißkapazität

Dimensionen (H x B x T in mm)

Material / Schutzklasse

Quelle(n)

CCM NVt 40

864

1455 x 400 x 310

Aluminium / IP55, IK10

   

CCM NVt 80

1.872

1455 x 750 x 310

Aluminium / IP55, IK10

   

CCM NVt 110

5.760

1455 x 1150 x 400

Aluminium / IP55, IK10

   

Hexatronic NBD117102/24

648

858 x 425 x 300 (ohne Sockel)

Polycarbonat / Al-Rahmen

   

R&M HD KVz SCM 82

1.728

(Nicht spezifiziert)

Polycarbonat

   

Diese Tabelle verdeutlicht die Skalierbarkeit der passiven Infrastruktur. Je nach Dichte des zu versorgenden Gebiets können Netzbetreiber wie die Deutsche Glasfaser unterschiedlich große Verteiler einsetzen, um die Investition präzise an den Bedarf anzupassen.

4.0 Das Zugangsnetz: Die finale Verbindung zum Gebäude
4.1 Bautechnik: Moderne und minimalinvasive Installationsmethoden
Ein entscheidender Faktor für die Geschwindigkeit und Akzeptanz des Glasfaserausbaus sind die eingesetzten Bauverfahren. Die Deutsche Glasfaser und ihre Baupartner setzen auf moderne, minimalinvasive Techniken, um die Bauzeiten zu verkürzen und die Beeinträchtigung für Anwohner und Umwelt so gering wie möglich zu halten.   

Zu den primär genutzten Verfahren gehören:

Fräsverfahren: Hierbei wird mit einer speziellen Fräse nur ein schmaler Schlitz (wenige Zentimeter breit) in befestigte Oberflächen wie Asphalt oder Pflaster geschnitten. In diesen Schlitz werden die Leerrohre (Mikrorohre) für die Glasfaser eingelegt, woraufhin der Schlitz sofort wieder professionell verschlossen wird. Dieses Verfahren ist extrem schnell und effizient.   

Spülbohrverfahren (Horizontal Directional Drilling, HDD): Dieses grabenlose Verfahren wird eingesetzt, um Hindernisse wie Straßen, Flüsse oder schützenswerte Grünflächen zu unterqueren. Es erfordert lediglich eine kleine Start- und eine Zielgrube, zwischen denen ein ferngesteuerter Bohrkopf einen unterirdischen Kanal für die Leerrohre schafft.   

Erdrakete (Impact Mole): Dies ist das bevorzugte Verfahren für die letzte Etappe, den Hausanschluss vom Gehweg zum Gebäude. Eine pneumatisch angetriebene "Rakete" verdrängt das Erdreich und zieht dabei das Leerrohr hinter sich her. Dadurch müssen Gärten und Einfahrten nicht aufgegraben werden.   

4.2 Inhouse-Architektur: Von der Hauswand bis zum Router
Innerhalb des Gebäudes folgt die Installation einem klaren, standardisierten Prozess mit definierten Komponenten, um eine gleichbleibend hohe Qualität und eine klare Trennung der Verantwortlichkeiten zu gewährleisten.   

4.2.1 Hausübergabepunkt (HÜP): Der passive Eintrittspunkt
Das von der Straße kommende Glasfaserkabel endet im Hausübergabepunkt (HÜP). Dies ist eine kleine, passive Anschlussbox (typische Maße ca. 16×9×3,5 cm), die im Inneren des Gebäudes, in der Regel nicht weiter als 3 Meter von der Hauseinführung entfernt, montiert wird. Meist befindet sich der HÜP im Keller oder im Hausanschlussraum. Er markiert den offiziellen Übergabepunkt vom öffentlichen Netz des Betreibers (Netzebene 3) in das private Hausnetz des Kunden (Netzebene 4).   

4.2.2 Glasfaser-Teilnehmeranschluss (GF-TA) und Netzabschluss (NT/ONT)
Die Signale werden vom HÜP zu den Endgeräten des Kunden weitergeleitet.

Glasfaser-Teilnehmeranschluss (GF-TA): Dies ist die eigentliche Glasfaserdose in der Wohnung, vergleichbar mit einer herkömmlichen Netzwerk- oder Telefondose. Der Installationsort wird bei der Hausbegehung mit dem Kunden abgestimmt und befindet sich idealerweise dort, wo später der Router platziert werden soll, z.B. im Wohnzimmer.   

Verbindungsweg (HÜP zu GF-TA): Für die Verbindung zwischen HÜP und GF-TA stellt die Deutsche Glasfaser ein Glasfaser-Patchkabel von bis zu 20 Metern Länge (in Einfamilienhäusern) bzw. 30 Metern (in Mehrfamilienhäusern) zur Verfügung. Der Kunde ist dafür verantwortlich, den Leitungsweg für dieses Kabel vorzubereiten. Dies geschieht typischerweise durch die Installation eines Leerrohrs. Dieses Leerrohr muss einen glatten Innenverlauf (keine Riffelung) und einen Mindestinnendurchmesser von 10 mm aufweisen.   

Netzabschluss (NT) / Optical Network Terminal (ONT): Dies ist das aktive Gerät, das das ankommende Lichtsignal in ein elektrisches Ethernet-Signal umwandelt. Der NT (oder ONT) wird vom Techniker direkt neben dem GF-TA (im Abstand von 0,3 bis 0,5 m) installiert und benötigt eine 230-V-Steckdose in der Nähe (innerhalb von 1,2 m). Dieses Gerät ist die letzte Komponente, die zur Infrastruktur der Deutschen Glasfaser gehört.   

4.2.3 Kunden-Router und hausinterne Verkabelung
Der Router des Kunden wird über ein Standard-LAN-Kabel mit dem NT/ONT verbunden. Ab diesem Punkt ist der Kunde für die weitere Verteilung des Internetsignals im Haus verantwortlich, sei es über weitere LAN-Kabel oder über WLAN. Die Deutsche Glasfaser bietet vorkonfigurierte Miet-Router an, es steht den Kunden jedoch frei, eigene, kompatible Router zu verwenden.   

4.3 Architekturbild 2: Schematische Darstellung der Inhouse-Installation
Die Installation lässt sich für die beiden häufigsten Wohnformen wie folgt visualisieren:

Einfamilienhaus (EFH): Die Glasfaser wird von der Straße mittels Erdrakete zum Haus geführt. Nach der Hauseinführung wird im Keller der HÜP installiert. Von dort verlegt der Kunde ein Leerrohr (bis zu 20 m) zum gewünschten Standort im Wohnbereich (z.B. Wohnzimmer). Am Ende des Leerrohrs installiert der DG-Techniker den GF-TA und direkt daneben den NT. Der Kunde schließt seinen Router per LAN-Kabel an den NT an.

Mehrfamilienhaus (MFH): Die Glasfaser wird zentral ins Gebäude geführt, wo im Keller oder einem Technikraum der HÜP installiert wird. Von diesem HÜP aus wird für jede einzelne Wohnung eine separate Glasfaserleitung verlegt. Diese dedizierte Faser endet in der jeweiligen Wohnung am GF-TA, an dem der NT angeschlossen wird. Dieses Vorgehen stellt sicher, dass jeder Haushalt im Gebäude einen echten, eigenen FTTH-Anschluss erhält und sich die Bandbreite nicht mit den Nachbarn im selben Haus teilt.   

5.0 Technischer Deep Dive: Konkrete Parameter und Protokolle
5.1 Passive Optical Network (PON) Technologien
Die Deutsche Glasfaser setzt auf einen klaren technologischen Migrationspfad, um die Zukunftsfähigkeit ihres Netzes zu gewährleisten.

5.1.1 GPON (ITU-T G.984): Der etablierte Standard
GPON (Gigabit Passive Optical Network) ist die in Deutschland am weitesten verbreitete PON-Technologie und bildete lange die Grundlage des DG-Netzes.   

Technologie: Es handelt sich um ein geteiltes Medium (Shared Medium), das auf dem Zeitmultiplexverfahren (Time Division Multiple Access, TDMA) basiert, bei dem jedem Endgerät (ONT) feste Zeitschlitze für die Übertragung zugewiesen werden.   

Bandbreite: Die Bandbreite ist asymmetrisch. Ein einzelner Port am OLT stellt eine Gesamtbandbreite von 2,488 Gbit/s Downstream (vom Anbieter zum Kunden) und 1,244 Gbit/s Upstream (vom Kunden zum Anbieter) zur Verfügung, die sich alle an diesen Port angeschlossenen Nutzer teilen.   

Wellenlängen: Um eine störungsfreie bidirektionale Kommunikation auf einer einzigen Faser zu ermöglichen, wird Wellenlängenmultiplex (Wavelength Division Multiplexing, WDM) eingesetzt. Der Downstream wird im Wellenlängenband um 1490 nm übertragen, während der Upstream das Band um 1310 nm nutzt.   

5.1.2 XGS-PON (ITU-T G.9807.1): Die 10-Gigabit-Zukunft
Seit April 2024 setzt die Deutsche Glasfaser, in Partnerschaft mit Nokia, bei Neuausbauten standardmäßig auf XGS-PON.   

Technologie: Der Name steht für 10-Gigabit-Symmetric-PON.

Bandbreite: Wie der Name andeutet, ist die Bandbreite symmetrisch. Ein OLT-Port liefert eine geteilte Gesamtbandbreite von ca. 10 Gbit/s im Downstream und 10 Gbit/s im Upstream (exakt: 9,953 Gbit/s).   

Wellenlängen: Um die Koexistenz mit GPON zu ermöglichen, nutzt XGS-PON andere Wellenlängen. Der Downstream liegt im Band um 1577 nm, der Upstream im Band um 1270 nm.   

5.1.3 Tabelle: Wellenlängenplan für die Koexistenz von GPON und XGS-PON
Die Nutzung unterschiedlicher Wellenlängen ist der Schlüssel zur Zukunftsfähigkeit der passiven Infrastruktur. Sie erlaubt es der DG, an derselben Glasfaser gleichzeitig Kunden mit GPON- und XGS-PON-Technologie zu versorgen. Ein einfacher Tausch der Endgeräte (ONT beim Kunden, Port-Karte am OLT) genügt für ein Upgrade, ohne dass die teure Tiefbauinfrastruktur angefasst werden muss.

Technologie

Richtung

Wellenlänge (nm)

Status im DG-Netz

GPON

Downstream (OLT → ONT)

1490

Weit verbreitet (Bestandsnetz)

Upstream (ONT → OLT)

1310

Weit verbreitet (Bestandsnetz)

XGS-PON

Downstream (OLT → ONT)

1577

Neuer Standard (seit 2024)

Upstream (ONT → OLT)

1270

Neuer Standard (seit 2024)


In Google Sheets exportieren
5.2 Kritische optische Designparameter
5.2.1 Splitter-Architektur: Topologie und typische Verhältnisse
Die passiven optischen Splitter, die in den NVt/DP-Gehäusen untergebracht sind, sind das Herzstück der Punkt-zu-Mehrpunkt-Architektur. Während der GPON-Standard theoretisch Split-Verhältnisse von bis zu 1:128 erlaubt , hat sich in der Praxis bei der Deutschen Glasfaser und anderen deutschen Netzbetreibern ein    

maximales Split-Verhältnis von 1:32 als De-facto-Standard etabliert.   

Dieses Verhältnis ist das Ergebnis einer wichtigen ingenieurtechnischen Abwägung. Ein höheres Split-Verhältnis (z.B. 1:64) würde die Kosten senken, da weniger teure OLT-Ports im PoP benötigt würden, um dieselbe Anzahl von Kunden zu versorgen. Gleichzeitig würde es aber die pro Nutzer verfügbare Bandbreite weiter aufteilen und die Signaldämpfung auf der Strecke erhöhen, was die Reichweite begrenzt. Das 1:32-Verhältnis bietet einen optimalen Kompromiss aus Kosteneffizienz und garantierter Leistungsfähigkeit. In manchen Fällen werden Splitter kaskadiert (z.B. ein 1:8-Splitter im Hauptverteiler gefolgt von einem 1:4-Splitter näher am Kunden), um die Topologie an die geografische Verteilung der Haushalte anzupassen, wobei das Gesamtverhältnis von 1:32 in der Regel nicht überschritten wird.   

5.2.2 Das optische Leistungsbudget: Eine praktische Berechnung
Das optische Leistungsbudget (Optical Power Budget) ist die maximale Signaldämpfung (Verlust an Lichtleistung), die eine Verbindung zwischen dem OLT und dem ONT tolerieren kann, bevor die Datenübertragung fehlerhaft wird oder ganz abbricht. Es wird in Dezibel (dB) gemessen.

GPON-Equipment wird in Leistungsklassen eingeteilt. Class B+ erlaubt eine Gesamtdämpfung von 28 dB, während die leistungsfähigere Class C+ bis zu 32 dB toleriert. Für Neuausbauten ist die Verwendung von Class C+ oder höher wahrscheinlich, um ausreichend Reserven für längere Strecken und zukünftige Alterungseffekte zu haben.   

Dieses Budget wird durch verschiedene Faktoren auf der Strecke verbraucht:

Splitter-Dämpfung: Dies ist der größte einzelne Verlustfaktor. Ein symmetrischer 1:32-Splitter verursacht eine typische Einfügedämpfung von ca. 17,8 dB.   

Faserdämpfung: Die Glasfaser selbst dämpft das Signal. Bei den relevanten Wellenlängen beträgt der Verlust ca. 0,35 bis 0,4 dB pro Kilometer.   

Stecker-Dämpfung: Jede Steckverbindung (z.B. am ODF, DP, HÜP) fügt eine Dämpfung von ca. 0,5 dB hinzu.

Spleiß-Dämpfung: Jede Schweißverbindung (Spleiß) zwischen zwei Fasern verursacht einen geringen Verlust von ca. 0,1 dB.   

Wartungsmarge: Planer inkludieren eine Sicherheitsreserve von 2,5 bis 3,0 dB, um Alterungseffekte, zukünftige Reparaturen (zusätzliche Spleiße) und Messungenauigkeiten abzudecken.   

5.2.3 Tabelle: Beispielrechnung für ein optisches Leistungsbudget im DG-Netz
Die folgende Tabelle zeigt eine beispielhafte Berechnung für eine typische GPON-Verbindung im Netz der Deutschen Glasfaser. Sie verdeutlicht, wie die einzelnen Komponenten das Gesamtbudget beeinflussen und wie daraus die maximale Reichweite des Netzes resultiert.

Parameter

Wert (dB/dBm)

Kumulativer Verlust (dB)

Anmerkungen

OLT Sendeleistung (Class C+)

+5,0 dBm

-

Typischer Wert für einen Class C+ Transceiver    

ONT Empfindlichkeit (min.)

-30,0 dBm

-

Typischer Wert für einen empfindlichen Empfänger    

Verfügbares Gesamtbudget

35,0 dB

0,0

Die maximal tolerierbare Dämpfung auf der Strecke.

Verlust: 1:32 Splitter

-17,8 dB

17,8

Typische Einfügedämpfung eines PLC-Splitters    

Verlust: Steckverbindungen (4x)

-2,0 dB

19,8

Annahme: PoP, DP-Eingang, DP-Ausgang, HÜP/GF-TA @ 0,5 dB

Verlust: Spleiße (2x)

-0,2 dB

20,0

Annahme: 1x im Feeder-, 1x im Verteilkabel @ 0,1 dB

Verlust: Wartungsmarge

-3,0 dB

23,0

Sicherheitsreserve für Reparaturen und Alterung

Verbleibendes Budget für Faser

12,0 dB

35,0

Budget, das für die distanzabhängige Dämpfung übrig bleibt

Maximale Netzreichweite

30 km

-

Kalkulation: 12,0 dB/0,4 dB/km. Liegt deutlich über der praktischen GPON-Grenze von 20 km.

Diese Berechnung zeigt, dass die Architektur der Deutschen Glasfaser mit einem 1:32-Split und Class-C+-Optiken über ein robustes Leistungsbudget verfügt, das auch in ausgedehnten ländlichen Gebieten eine zuverlässige Verbindung sicherstellt.

5.3 Punkt-zu-Punkt (PtP) Active Ethernet für Geschäftskunden
Parallel zur PON-Infrastruktur betreibt die Deutsche Glasfaser ein PtP-Netz für Geschäftskunden. Hierbei handelt es sich um ein aktives optisches Netz (AON), das jedem Kunden eine dedizierte, ungeteilte Glasfaserverbindung von seinem Standort bis zu einem dedizierten Port an einem aktiven Switch im PoP bereitstellt. Als Hardware kommen hierfür beispielsweise Nokia 7360 ISAM-Systeme mit den Leitungskarten NELT-B oder FELT-C zum Einsatz, während auf Kundenseite Netzabschlussgeräte (NTs) wie der Nokia 7210 SAS-K oder der Cisco NCS 520 installiert werden. Diese Architektur ist die Grundlage für symmetrische Multi-Gigabit-Dienste und für Kunden, die auf garantierte Bandbreiten und höchste Verfügbarkeit angewiesen sind, unerlässlich.   

5.4 Layer-2/3-Protokolle und Dienstbereitstellung
Zugangsprotokolle: Die Deutsche Glasfaser unterstützt sowohl IPoE (IP over Ethernet), bei dem die IP-Adressvergabe über DHCP erfolgt, als auch das klassische PPPoE (Point-to-Point Protocol over Ethernet). IPoE gilt als die modernere und effizientere Methode.   

VLANs: Virtuelle LANs (VLANs) werden eingesetzt, um den Datenverkehr verschiedener Kunden und Dienste (z.B. Internet, VoIP-Telefonie, TV) logisch voneinander zu trennen, obwohl sie über dieselbe physische Infrastruktur laufen.   

Management: Die Netzabschlussgeräte beim Kunden (ONTs) werden zentral vom Managementsystem der Deutschen Glasfaser über das OMCI-Protokoll (ONU Management and Control Interface) nach ITU-T G.988 verwaltet. Dies ermöglicht die Fernkonfiguration, Überwachung und Fehlerdiagnose. Die Authentifizierung eines neuen Geräts im Netz erfolgt dabei über dessen eindeutige Seriennummer.   

6.0 Analyse, Einblicke und Zukunftsausblick
6.1 Architektonische Abwägungen: PON vs. AON im Kontext der Deutschen Glasfaser
Die Entscheidung der Deutschen Glasfaser, sowohl eine PON- als auch eine AON-Architektur zu betreiben, ist kein Kompromiss, sondern eine bewusste strategische Optimierung. Jede Technologie wird dort eingesetzt, wo ihre Stärken am besten zur Geltung kommen.

PON (Punkt-zu-Mehrpunkt): Die Stärken dieser Technologie liegen in den niedrigen Betriebskosten, der hohen Skalierbarkeit für eine große Anzahl von Nutzern und der Kosteneffizienz bei der Erschließung von Wohngebieten. Die Nachteile, wie das geteilte Medium und die damit verbundene Bandbreitenkonkurrenz sowie eine komplexere Fehlersuche, werden durch die enormen Kostenvorteile im Privatkundensegment mehr als aufgewogen.   

AON (Punkt-zu-Punkt): Diese Architektur bietet dedizierte, garantierte Bandbreite, eine einfache Fehlerisolierung pro Kunde und eine simple Verwaltung. Dem stehen jedoch hohe Investitionskosten (ein Switch-Port pro Kunde) und höhere Betriebskosten (Strom und Kühlung für die aktive Technik im PoP) gegenüber. Dies macht sie zur idealen Lösung für das margenstärkere Geschäftskundensegment, wo Zuverlässigkeit und garantierte Leistung entscheidend sind.   

Die hybride Strategie der DG ermöglicht es, die für jeden Marktsektor am besten geeignete Technologie einzusetzen und so ein finanziell nachhaltiges Netzwerk in den Zielregionen aufzubauen.

6.2 Zentrale Stärken: Skalierbarkeit, Kosteneffizienz und Zukunftssicherheit
Die Architektur der Deutschen Glasfaser zeichnet sich durch drei wesentliche Stärken aus:

Skalierbarkeit: Das modulare Design, von den verschiedenen PoP- und NVt-Größen bis hin zu den standardisierten Bau- und Installationsprozessen, schafft ein industrielles "Fabrikmodell". Dieses Modell ermöglicht einen schnellen, wiederholbaren und hochgradig skalierbaren Rollout in neuen Gemeinden. Der Einsatz von spezialisierter Software wie IQGeo zur digitalen Planung, Bestandsdokumentation und Verwaltung der Materialstücklisten (BoM) ist ein entscheidender Faktor für diese Effizienz.   

Kosteneffizienz: Die starke Ausrichtung auf ein passives Netz (PON) minimiert die langfristigen Betriebskosten (OPEX) drastisch. Dies ist der entscheidende Faktor, der den Glasfaserausbau in ländlichen Gebieten mit geringerer Anschlussdichte überhaupt erst rentabel macht.

Zukunftssicherheit: Dies ist ein Eckpfeiler der DG-Architektur. Die grundlegende Entscheidung, Glasfaser konsequent bis in die Wohnung (FTTH) zu verlegen, bedeutet, dass die passive Infrastruktur – der teuerste und aufwendigste Teil des Netzes – für Jahrzehnte Bestand haben wird. Zukünftige Bandbreitenerhöhungen von GPON (1 Gbit/s) auf XGS-PON (10 Gbit/s) und darüber hinaus (z.B. 25G-PON) können durch einen reinen Austausch der aktiven Technik an den beiden Endpunkten (OLT im PoP und ONT beim Kunden) realisiert werden. Der durchdachte Wellenlängenplan stellt sicher, dass diese Upgrades ohne Eingriffe in die verlegte Faserinfrastruktur erfolgen können. Dies schützt den Großteil der getätigten Investition.   

6.3 Strategischer Ausblick: Technologische Modernisierung und Expansion
Die Deutsche Glasfaser verfolgt eine klare und aggressive Wachstumsstrategie, die durch ihre technologische und finanzielle Aufstellung untermauert wird. Die Partnerschaft mit Nokia, die im Mai 2024 bekannt gegeben wurde, ist der zentrale technologische Hebel für den Übergang zu einem Multi-Gigabit-Netz, das auf XGS-PON als neuem Standard basiert.   

Parallel dazu wird die Einführung des neuen, effizienteren "Central Office"-Konzepts die Kosten weiter senken und die Ausbaugeschwindigkeit erhöhen. Dies ist eine notwendige Voraussetzung, um die ambitionierten Ausbauziele zu erreichen, die eine Versorgung von bis zu 6 Millionen Haushalten vorsehen.   

Die finanzielle Basis für diese massive Expansion ist durch umfangreiche Finanzierungsrunden gesichert, die ein Fremdkapitalvolumen von über 7 Milliarden Euro umfassen. Die Beteiligung der Europäischen Investitionsbank (EIB) mit signifikanten Darlehen unterstreicht die strategische und volkswirtschaftliche Bedeutung der Erschließung unterversorgter Gebiete durch die Deutsche Glasfaser.   

Zusammenfassend lässt sich sagen, dass das Netzwerk der Deutschen Glasfaser mehr ist als nur eine Ansammlung von Technologien. Es ist ein kohärentes Gesamtsystem, in dem strategische, finanzielle und technische Entscheidungen eng miteinander verknüpft sind. Der Erfolg des Unternehmens beruht auf der konsequenten Optimierung des gesamten Ausbaumodells für ein spezifisches, lange vernachlässigtes Marktsegment. Der größte Wettbewerbsvorteil ist nicht eine einzelne Technologie, sondern der industrialisierte Prozess, mit dem diese Technologie in großem Maßstab effizient und kostengünstig eingesetzt wird.

7.0 Anhang
7.1 Glossar der wichtigsten Begriffe und Abkürzungen
Akronym

Vollständiger Name

Deutsche Entsprechung / Beschreibung

AON

Active Optical Network

Aktives optisches Netz. Netzarchitektur mit aktiven (stromversorgten) Komponenten im Verteilnetz. Bietet dedizierte Verbindungen (PtP).

DP

Distribution Point

Verteilungspunkt. Bezeichnung der DG für einen Unterverteiler im Straßenbereich (entspricht NVt).

FTTH

Fiber to the Home

Glasfaser bis in die Wohnung. Die leistungsfähigste Ausbauart, bei der die Glasfaser direkt beim Endkunden endet.

GF-TA

Glasfaser-Teilnehmeranschluss

Die Glasfaser-Anschlussdose in der Wohnung des Kunden.

GPON

Gigabit Passive Optical Network

Gigabit-fähiges passives optisches Netz. Etablierter PON-Standard (ITU-T G.984) mit asymmetrischer Bandbreite (2,5/1,25 Gbit/s).

HÜP

Hausübergabepunkt

Der Punkt, an dem das Glasfaserkabel ins Gebäude eintritt und vom öffentlichen Netz an das Hausnetz übergeben wird.

IPoE

IP over Ethernet

Zugangsprotokoll, bei dem die IP-Konfiguration per DHCP erfolgt. Gilt als moderner als PPPoE.

IXP

Internet Exchange Point

Internet-Austauschknoten. Physische Infrastruktur, an der sich Internetanbieter verbinden, um Datenverkehr auszutauschen.

KVz

Kabelverzweiger

Ältere Bezeichnung für einen passiven Verteilerschrank am Straßenrand. Heute als NVt bezeichnet.

NT

Network Termination

Netzabschluss. Aktives Gerät, das das Glasfasersignal in ein elektrisches Ethernet-Signal umwandelt. Siehe ONT.

NVt

Netzverteiler

Moderner Begriff für einen passiven Verteilerschrank am Straßenrand, der Spleiße und/oder Splitter enthält.

ODF

Optical Distribution Frame

Optischer Verteilerrahmen. Passives Gestell im PoP zum Rangieren und Verbinden von Glasfasern.

OLT

Optical Line Terminal

Optischer Leitungsendpunkt. Aktives Gerät im PoP, das die Kopfstation des PON-Netzes bildet.

OMCI

ONU Management and Control Interface

Protokoll zur Fernverwaltung und -konfiguration der Endgeräte (ONTs) durch den Netzbetreiber.

ONT

Optical Network Terminal

Optischer Netzabschluss. Das aktive Endgerät beim Kunden, das Licht in elektrische Signale umwandelt. Siehe NT.

PON

Passive Optical Network

Passives optisches Netz. Netzarchitektur, die ohne aktive Komponenten im Verteilnetz auskommt und auf Splittern basiert (PtMP).

PoP

Point of Presence

Zentraler Netzknotenpunkt oder Hauptverteiler für eine Gemeinde oder ein größeres Gebiet.

PPPoE

Point-to-Point Protocol over Ethernet

Klassisches Zugangsprotokoll, das eine logische Punkt-zu-Punkt-Verbindung über Ethernet aufbaut.

PtP

Point-to-Point

Punkt-zu-Punkt. Eine Netzwerktopologie, bei der jeder Endpunkt eine dedizierte Verbindung zum zentralen Knoten hat (entspricht AON).

WDM

Wavelength Division Multiplexing

Wellenlängenmultiplexverfahren. Technik, um mehrere Datensignale gleichzeitig über eine einzige Faser zu senden, indem unterschiedliche Lichtfarben (Wellenlängen) verwendet werden.

XGS-PON

10-Gigabit-capable Symmetric PON

10-Gigabit-fähiges symmetrisches passives optisches Netz. Moderner PON-Standard (ITU-T G.9807.1) mit symmetrischer Bandbreite (∼10/10 Gbit/s).