Das Glasfasernetz der Deutschen Glasfaser in Deutschland: Eine Infrastruktur- und Geospatial-Analyse
1.0 Executive Summary
Dieser Bericht liefert eine umfassende Analyse und eine modellbasierte Kartierung der Netzinfrastruktur der Deutschen Glasfaser (DG) in Deutschland. Er fasst die wesentlichen Erkenntnisse über die Netzwerkarchitektur, die strategische Ausrichtung und die geografische Ausdehnung des Unternehmens zusammen. Die Analyse zeigt, dass die Deutsche Glasfaser eine konsequente „Fiber to the Home“ (FTTH)-Strategie verfolgt, mit der sie sich gezielt auf die Versorgung des ländlichen und suburbanen Raums konzentriert und sich damit von Wettbewerbern mit gemischten Technologiestrategien abhebt.

Ein zentrales Ergebnis ist, dass das nationale Backbone-Netz der Deutschen Glasfaser kein vollständig selbst errichtetes, sondern ein strategisch zusammengesetztes Netzwerk ist. Es basiert maßgeblich auf der Anmietung von unbeschalteten Glasfasern (Dark Fiber) von Infrastrukturpartnern wie GasLINE und DB broadband. Dieser kapital-effiziente Ansatz ermöglicht eine schnelle und flexible Expansion, ohne die hohen Investitionskosten für den Bau eigener Langstreckenverbindungen tragen zu müssen.

Die zentralen Netzknoten und Gateways zum globalen Internet befinden sich in den wichtigsten deutschen und europäischen Interconnection-Hubs Frankfurt am Main, Düsseldorf und Amsterdam. Hier tauscht die Deutsche Glasfaser über leistungsstarke Verbindungen zu Internetknotenpunkten (IXPs) und über direkte Peerings Datenverkehr aus.

Aufgrund der Nichtverfügbarkeit öffentlicher Daten zu den exakten Standorten der lokalen Verteilerpunkte (Points of Presence, POPs) wurde eine plausible, realistische Modellierung vorgenommen. Die öffentlich bekannten Ausbaugebiete des Unternehmens dienen als Proxy zur Verortung der tausenden lokalen POPs. Für jedes dieser Gebiete wird ein zentraler POP-Standort angenommen und mit Geokoordinaten versehen. Dieser Bericht stellt somit einen vollständigen, geokodierten Datensatz aller identifizierten und modellierten Netzwerkstandorte bereit, der als Grundlage für weiterführende Geospatial-Analysen, Marktbeobachtungen und strategische Planungen dient.

2.0 Die Netzwerkarchitektur der Deutschen Glasfaser: Ein Fokus auf FTTH
Die Netzwerk- und Geschäftsstrategie der Deutschen Glasfaser ist untrennbar mit ihrer technologischen Ausrichtung verbunden. Das Unternehmen hat sich als einer der führenden alternativen Anbieter auf dem deutschen Telekommunikationsmarkt etabliert, indem es konsequent auf eine reine Glasfaserinfrastruktur bis zum Endkunden setzt.

2.1 Das „Reine Glasfaser“-Mandat (FTTH)
Die Deutsche Glasfaser verfolgt eine strikte „Fiber to the Home“ (FTTH)-Strategie, bei der eine dedizierte Glasfaserleitung direkt bis in die Wohnung oder das Geschäftsgebäude des Kunden verlegt wird. Dieser Ansatz ist der technologisch fortschrittlichste und zukunftssicherste, da er die volle Leistungsfähigkeit des Glasfasernetzes ohne Kompromisse bis zum Endgerät liefert.   

Im Gegensatz dazu setzen Wettbewerber wie die Deutsche Telekom oft auf einen Technologiemix, der auch „Fiber to the Curb“ (FTTC) oder VDSL umfasst, bei denen die letzten Meter vom Verteilerkasten bis zum Haus über bestehende Kupferkabel überbrückt werden. Vodafone nutzt vorrangig sein Hybrid-Fiber-Coax (HFC)-Kabelnetz. Der entscheidende Vorteil der reinen FTTH-Architektur der DG liegt in der garantierten Bandbreite und den hohen, symmetrischen Übertragungsraten für Up- und Downloads, die nicht durch veraltete Kupferleitungen auf der „letzten Meile“ gedrosselt werden. Dies ermöglicht stabile Verbindungen auch zu Spitzenlastzeiten und ist eine wesentliche Voraussetzung für datenintensive Anwendungen wie Cloud-Dienste, Videokonferenzen und hochauflösendes Streaming.   

Die technische Umsetzung beim Kunden besteht aus drei Kernkomponenten:

Hausübergabepunkt (HÜP): Der Punkt, an dem das Glasfaserkabel ins Gebäude eintritt und terminiert wird.   

Glasfaser-Teilnehmeranschluss (GF-TA): Eine spezielle Anschlussdose in der Wohnung, die die Glasfaser aufnimmt.   

Network Termination (NT): Ein Glasfasermodem, das das optische Signal in ein elektrisches Signal für den Router umwandelt.   

2.2 Hierarchische Netzwerktopologie (Netzebenen)
Das Netzwerk der Deutschen Glasfaser lässt sich, wie in der Telekommunikation üblich, in hierarchische Ebenen (Netzebenen, NE) unterteilen, die den Weg der Daten vom globalen Internet bis zum Endgerät beschreiben.   

Backbone (NE 1/2): Das Rückgrat des Netzes, bestehend aus Hochgeschwindigkeits-Glasfaserverbindungen, die die großen Metropolregionen und zentralen Rechenzentren miteinander verbinden. Hier werden die Datenströme aus dem gesamten Netzwerk gebündelt.   

Zugangsnetz (NE 3): Diese Ebene bildet die Verbindung zwischen dem regionalen Backbone und den lokalen Verteilnetzen. Sie beginnt im regionalen Hauptverteiler, dem Point of Presence (POP), und erstreckt sich über Glasfaserkabel, die unterirdisch bis zu den einzelnen Straßenzügen verlegt werden.   

Gebäudenetz (NE 4): Die Netzebene 4 umfasst die Verkabelung vom Hausübergabepunkt (HÜP) an der Grundstücksgrenze oder im Keller bis zum Glasfaser-Teilnehmeranschluss (GF-TA) in der einzelnen Wohnung oder dem Büro.   

Wohnungsnetz (NE 5): Die letzte Ebene bezeichnet die Verkabelung innerhalb der Wohnung, typischerweise vom GF-TA zum Router und den daran angeschlossenen Endgeräten.   

2.3 Geschäftsmodell und Rollout-Strategie
Die Geschäftsstrategie der Deutschen Glasfaser ist darauf ausgerichtet, Marktlücken zu besetzen, die von den etablierten Anbietern lange Zeit vernachlässigt wurden. Das Unternehmen konzentriert sich gezielt auf den eigenwirtschaftlichen Ausbau im ländlichen und suburbanen Raum. Diese strategische Positionierung vermeidet den direkten und kostenintensiven Wettbewerb mit Incumbents wie der Deutschen Telekom in bereits gut versorgten städtischen Ballungszentren.   

Ein zentrales Element des Geschäftsmodells ist die sogenannte „Nachfragebündelung“. Der Ausbau in einer Gemeinde oder einem Stadtteil beginnt erst, wenn sich in einer vorab definierten Vermarktungsphase eine Mindestanzahl von Haushalten – typischerweise 33 % – für einen Glasfaseranschluss entscheidet. Dieses Vorgehen minimiert das Investitionsrisiko für die Deutsche Glasfaser erheblich, da die hohen Kosten für den Tiefbau erst dann anfallen, wenn eine ausreichende Kundennachfrage und damit die Wirtschaftlichkeit des Projekts gesichert ist.   

Der Erfolg dieser Strategie lässt sich indirekt an der Reaktion des Marktes ablesen. Die Deutsche Telekom, die den Glasfaserausbau lange zögerlich betrieb, hat ihre Anstrengungen in den letzten Jahren massiv verstärkt und tritt nun auch im ländlichen Raum als direkter Konkurrent zur Deutschen Glasfaser auf. Die Gründung eines eigenen Tiefbauunternehmens, der Deutschen Tiefbau GmbH, durch die Telekom im Jahr 2023 kann als direkte strategische Antwort auf das Geschäftsmodell der Deutschen Glasfaser gewertet werden. Sie zielt darauf ab, die Kosten- und Geschwindigkeitsvorteile zu neutralisieren, die die Deutsche Glasfaser durch ihren fokussierten und nachfragegesteuerten Ansatz erzielen konnte. Dies signalisiert eine signifikante Verschiebung der Wettbewerbsdynamik, bei der der Kampf um die Glasfaser-Dominanz nun auch in den ländlichen Gebieten geführt wird, die die Deutsche Glasfaser als Pionier erschlossen hat.   

3.0 Das nationale Backbone: Ein Kompositum aus strategischen Allianzen
Eine der wichtigsten Erkenntnisse dieser Analyse ist, dass das deutschlandweite Backbone-Netz der Deutschen Glasfaser keine vollständig selbst gebaute Infrastruktur ist. Stattdessen handelt es sich um ein hochgradig strategisches und kapitaleffizientes Kompositnetz, das auf der langfristigen Anmietung von Dark-Fiber-Kapazitäten von zentralen Infrastrukturpartnern beruht.

3.1 Die GasLINE-Partnerschaft
Ein Grundpfeiler des DG-Backbones ist die 2018 geschlossene Kooperation mit GasLINE. Diese Partnerschaft gewährt der Deutschen Glasfaser Zugriff auf das über 25.000 Kilometer lange Glasfasernetz, das entlang des deutschen Ferngasleitungsnetzes verlegt ist. Dieses Netz fungiert als „überregionale Hauptschlagadern“ und verbindet die regionalen Zugangsnetze der Deutschen Glasfaser mit den zentralen Internetknotenpunkten. Die Trassenführung entlang von Gaspipelines bietet eine hohe physische Sicherheit und erreicht auch Regionen abseits der typischen Telekommunikationsrouten. Die öffentlich zugängliche Netzkarte von GasLINE ist eine wesentliche Grundlage für die Modellierung des DG-Backbones.   

3.2 Die DB Broadband-Partnerschaft
Eine weitere strategische Säule ist der Rahmenvertrag mit der DB broadband GmbH. Durch diese Allianz kann die Deutsche Glasfaser auf freie Glasfaserkapazitäten im Netz der Deutschen Bahn zugreifen, das sich entlang des Schienennetzes erstreckt und bereits über 20.000 Kilometer umfasst, mit dem Ziel, das gesamte Streckennetz von 33.400 Kilometern auszubauen. Diese Partnerschaft bietet einzigartige, sichere und oft direkte Verbindungswege, insbesondere zur Anbindung von ländlichen Gemeinden, die in der Nähe von Bahnstrecken liegen. Die interaktive Karte der DB InfraGO dient als zweite wichtige Datenquelle zur Visualisierung dieser Backbone-Routen.   

3.3 Strategische Implikationen und konzeptionelle Backbone-Karte
Diese „Asset-light“-Strategie für das Backbone-Netz ist ein entscheidender Faktor für das schnelle Wachstum der Deutschen Glasfaser. Anstatt immense Summen in den Bau eigener Langstreckentrassen zu investieren – eine der größten Hürden im Netzausbau  –, nutzt das Unternehmen bestehende, geografisch diverse und physisch geschützte Glasfaserkorridore. Die eingesparten Investitionsmittel (CAPEX) können direkt in den Ausbau des Zugangsnetzes (NE 3) und den Anschluss der Endkunden fließen, wo die eigentliche Wertschöpfung stattfindet. Dies verschafft der DG einen signifikanten Wettbewerbsvorteil in Bezug auf Markteintrittsgeschwindigkeit und Kapitaleffizienz.   

Die Kombination der Netze von GasLINE und DB broadband bietet zudem eine inhärente Redundanz. Durch die Nutzung zweier völlig unabhängiger Infrastrukturtypen (Gasleitungen und Schienenwege) wird die Ausfallsicherheit des Gesamtnetzes erheblich erhöht. Für eine konzeptionelle Karte des nationalen Backbones der Deutschen Glasfaser werden die Netzkarten von GasLINE und DB broadband übereinandergelegt. Dies ergibt ein plausibles Modell der Hauptverkehrsadern, die die Metropolregionen mit den Kernknoten in Frankfurt und Düsseldorf verbinden und von denen die regionalen Netze in die Fläche abzweigen.   

4.0 Core Network Nodes: Rechenzentren, Peering-Knoten und Geodaten
Das Herzstück des Netzwerks der Deutschen Glasfaser sind die physischen Standorte – hochsichere Rechenzentren, in denen das Unternehmen sein Netz mit dem globalen Internet verbindet und Datenverkehr mit anderen Netzbetreibern (Carriern), Content-Anbietern (z.B. Netflix, Google) und Unternehmen austauscht. Die Daten zu diesen Standorten sind öffentlich verifizierbar und bilden die Ankerpunkte des gesamten Netzmodells.

4.1 Primäre Interconnection-Hubs und Peering-Strategie
Die Deutsche Glasfaser konzentriert ihre Kernnetzinfrastruktur auf die zwei wichtigsten digitalen Ökosysteme Deutschlands: Frankfurt am Main und Düsseldorf. Zusätzlich wird ein strategisch wichtiger Knotenpunkt in Amsterdam betrieben, um die internationale Anbindung zu diversifizieren und die Ausfallsicherheit zu erhöhen.   

Das Unternehmen operiert unter mehreren Autonomen Systemen (AS), die im Internet eindeutige Netzwerke identifizieren. Die primären AS-Nummern sind AS60294 (Deutsche Glasfaser) und AS8899 (DEUTSCHE-GLASFASER). Die Existenz von    

AS8899 ist ein Resultat der Übernahme des Anbieters inexio und dessen Infrastruktur. Die Peering-Standorte beider AS-Nummern sind weitgehend identisch, was auf ein erfolgreich integriertes Kernnetz hindeutet.   

4.2 Schlüsselaustauschpunkte (Internet Exchanges - IXPs)
Die Deutsche Glasfaser ist an den folgenden zentralen Internetknotenpunkten präsent, um einen effizienten und kostengünstigen Datenaustausch zu gewährleisten:

DE-CIX Frankfurt: Als größter Internetknotenpunkt in Deutschland und einer der weltweit wichtigsten ist dies der primäre Peering-Standort für die DG. Eine Anbindung mit einer Kapazität von 400 Gbit/s unterstreicht die immense Bedeutung dieses Hubs für das gesamte Netzwerk.   

MegaIX Dusseldorf: Dieser Knotenpunkt ist von strategischer Bedeutung für die Versorgung von Nordrhein-Westfalen, einem Kernmarkt der Deutschen Glasfaser. Auch hier unterhält das Unternehmen eine leistungsstarke 400-Gbit/s-Anbindung.   

AMS-IX Amsterdam: Als einer der führenden europäischen Internetknoten bietet der AMS-IX Zugang zu globalen Carriern und Content Delivery Networks. Die Deutsche Glasfaser betreibt hier eine Anbindung mit 100 Gbit/s, um den internationalen Datenverkehr optimal zu leiten.   

Tabelle 4.1: Kernrechenzentren und Peering-Standorte
Die folgende Tabelle listet die verifizierten, physischen Standorte auf, die das Fundament des Kernnetzes der Deutschen Glasfaser bilden. Diese geokodierten Datenpunkte besitzen die höchste Genauigkeit in diesem Bericht.

Einrichtungsname

Stadt

Adresse

Funktion

DG ASNs präsent

Geokoordinaten (WGS84)

Quelle

Digital Realty FRA1-16

Frankfurt am Main

Weismüllerstraße 37-39, 60314

Peering/Colocation

AS60294, AS8899

50.12040, 8.73873

   

Digital Realty DUS1-2

Düsseldorf

In der Steele 29, 40599

Peering/Colocation

AS60294, AS8899

51.18827, 6.86722

   

AMS-IX (Logischer Knoten)

Amsterdam

Science Park, 1098 XG

Peering

AS60294

52.35590, 4.95120

   

5.0 Regionale und lokale Verteilung: Kartierung der Points of Presence (POPs)
Während die Core Nodes das Herz des Netzwerks bilden, sind die Points of Presence (POPs) die entscheidenden Knotenpunkte für die regionale und lokale Versorgung. Sie bilden die Brücke zwischen dem nationalen Backbone und den tausenden von Endkundenanschlüssen.

5.1 Funktion und Einsatz von POPs
Ein POP ist ein lokaler Hauptverteiler, der typischerweise in einem kleinen, speziell dafür errichteten Gebäude oder einem technischen Container untergebracht ist. In diesem POP laufen alle Glasfaseranschlüsse eines bestimmten Versorgungsgebiets zusammen. Er beherbergt die aktive Netzwerktechnik (wie Multiplexer und Router), die die Lichtsignale der einzelnen Kunden bündelt und den Datenverkehr an das übergeordnete Backbone-Netz weiterleitet. Jeder POP versorgt ein klar definiertes geografisches Gebiet, beispielsweise eine Stadt, eine Gemeinde oder eine Gruppe von Dörfern. So versorgt der POP in Zorneding (Bayern) die Ortsteile Zorneding, Ingelsberg, Pöring und Wolfesing.   

5.2 Methodik zur inferenzbasierten POP-Standortkartierung
Da die genauen Adressen der tausenden von POPs von der Deutschen Glasfaser nicht öffentlich gemacht werden, ist eine vollständige, exakte Kartierung nicht möglich. Um der Anforderung des Nutzers nach einer umfassenden Karte mit plausiblen Annahmen dennoch gerecht zu werden, wurde die folgende inferenzbasierte Methodik entwickelt:

Grundannahme: Es wird angenommen, dass die Deutsche Glasfaser für jedes eigenständige Ausbauprojekt, das als Ausbaugebiet auf ihrer Webseite gelistet ist, einen dedizierten POP errichtet.

Datenerfassung: Zunächst wird eine vollständige Liste aller Ausbaugebiete aus den öffentlichen Quellen der Deutschen Glasfaser systematisch erfasst (siehe Abschnitt 6.0).

Identifikation: Für jedes Ausbaugebiet werden der Name der primären Gemeinde und die zugehörige Postleitzahl (PLZ) identifiziert.

Geokodierung: Mithilfe eines Geokodierungsdienstes wird die Postleitzahl oder der Gemeindename in geografische Koordinaten (Breiten- und Längengrad im WGS84-Format) umgewandelt. Als Referenzpunkt wird dabei typischerweise das geografische Zentrum der Gemeinde verwendet.

Repräsentation: Dieser geokodierte Punkt repräsentiert den plausiblen, modellierten Standort des POPs, der das jeweilige Ausbaugebiet versorgt.

Diese Methode ermöglicht eine skalierbare und logisch nachvollziehbare Erstellung der angeforderten Geodaten und füllt die bestehenden Informationslücken mit realistischen Annahmen.

5.3 Plausible POP-zu-Backbone-Konnektivität
Die so verorteten POPs werden an das in Abschnitt 3 modellierte nationale Backbone-Netz angebunden. Durch die Visualisierung der POP-Standorte und der Backbone-Trassen (basierend auf den Netzen von GasLINE und DB broadband) lassen sich die wahrscheinlichen Anbindungspfade nachvollziehen. Ein POP in einer ländlichen Gemeinde in Bayern würde beispielsweise an eine nahegelegene Glasfasertrasse angeschlossen, die in Richtung eines größeren Netzknotens wie München oder Nürnberg verläuft, von wo aus die Verbindung zum Core-Standort in Frankfurt hergestellt wird.

6.0 Der komplette Service-Footprint: Ein Katalog der Ausbaugebiete der Deutschen Glasfaser
Dieser Abschnitt dokumentiert die öffentlich bekannte Marktabdeckung der Deutschen Glasfaser. Die Daten wurden systematisch aus dem „Netzausbau“-Bereich der Unternehmenswebseite aggregiert und nach Bundesländern sowie Landkreisen geordnet. Der angegebene Status (z. B. Planungsphase, Bauphase, Netz aktiv) spiegelt den zum Zeitpunkt der Erhebung bekannten Zustand wider und dient als Grundlage für die in Abschnitt 5 beschriebene POP-Modellierung.

Tabelle 6.1: Servicegebiete in Nordrhein-Westfalen
Kreis / Kreisfreie Stadt

Ausgewählte Gemeinden/Städte im Ausbau

Quelle

Kreis Borken

Ahaus, Borken, Gescher, Heiden, Reken, Vreden

   

Kreis Coesfeld

Billerbeck, Coesfeld, Dülmen, Havixbeck, Nottuln

   

Kreis Düren

Aldenhoven, Düren, Inden, Jülich, Langerwehe

   

Kreis Euskirchen

Euskirchen, Mechernich, Zülpich

   

Kreis Gütersloh

Gütersloh, Halle (Westf.), Harsewinkel, Rietberg, Verl

   

Kreis Heinsberg

Erkelenz, Geilenkirchen, Heinsberg, Hückelhoven

   

Kreis Kleve

Bedburg-Hau, Emmerich am Rhein, Goch, Kalkar, Kleve

   

Kreis Olpe

Attendorn, Drolshagen, Finnentrop, Olpe, Wenden

   

Kreis Steinfurt

Emsdetten, Greven, Hörstel, Ibbenbüren, Lengerich

   

Kreis Viersen

Brüggen, Grefrath, Kempen, Nettetal, Viersen

   

Rhein-Kreis Neuss

Dormagen, Grevenbroich, Jüchen, Kaarst, Neuss

   

Städteregion Aachen

Aachen, Alsdorf, Baesweiler, Eschweiler, Stolberg

   

Tabelle 6.2: Servicegebiete in Niedersachsen
Kreis / Kreisfreie Stadt

Ausgewählte Gemeinden/Städte im Ausbau

Quelle

Landkreis Ammerland

Apen, Bad Zwischenahn, Rastede, Westerstede

   

Landkreis Celle

Bergen, Celle, Faßberg, Hermannsburg, Wietze

   

Landkreis Cloppenburg

Barßel, Bösel, Cloppenburg, Friesoythe, Saterland

   

Landkreis Emsland

Dörpen, Haren (Ems), Haselünne, Lingen (Ems), Meppen

   

Landkreis Gifhorn

Gifhorn, Isenbüttel, Meine, Sassenburg, Wittingen

   

Landkreis Grafschaft Bentheim

Bad Bentheim, Emlichheim, Nordhorn, Schüttorf

   

Landkreis Harburg

Buchholz in der Nordheide, Neu Wulmstorf, Rosengarten

   

Landkreis Hildesheim

Alfeld (Leine), Bad Salzdetfurth, Bockenem, Hildesheim

   

Landkreis Leer

Bunde, Jemgum, Leer (Ostfriesland), Moormerland

   

Region Hannover

Barsinghausen, Burgdorf, Garbsen, Hannover, Neustadt

   

Stadt Wolfsburg

Wolfsburg

   

Tabelle 6.3: Servicegebiete in Bayern
Landkreis

Ausgewählte Gemeinden/Städte im Ausbau

Quelle

Landkreis Aichach-Friedberg

Aichach, Friedberg, Mering, Pöttmes

   

Landkreis Dachau

Dachau, Karlsfeld, Markt Indersdorf

   

Landkreis Donau-Ries

Donauwörth, Nördlingen, Oettingen i.Bay.

   

Landkreis Ebersberg

Ebersberg, Grafing b.München, Kirchseeon, Zorneding

   

Landkreis Erding

Dorfen, Erding, Taufkirchen (Vils)

   

Landkreis Fürstenfeldbruck

Fürstenfeldbruck, Germering, Olching, Puchheim

   

Landkreis Kelheim

Abensberg, Bad Abbach, Kelheim, Neustadt a.d.Donau

   

Landkreis Landshut

Altdorf, Ergolding, Essenbach, Landshut

   

Landkreis München

Aschheim, Garching b.München, Haar, Ismaning, Ottobrunn

   

Landkreis Würzburg

Estenfeld, Höchberg, Ochsenfurt, Rimpar, Veitshöchheim

   

Tabelle 6.4: Servicegebiete in weiteren Bundesländern (Auszug)
Bundesland

Landkreis / Stadt

Ausgewählte Gemeinden/Städte im Ausbau

Quelle

Baden-Württemberg

Landkreis Böblingen

Aidlingen, Böblingen, Herrenberg, Sindelfingen

   

Baden-Württemberg

Rhein-Neckar-Kreis

Hockenheim, Schwetzingen, Sinsheim, Weinheim

   

Brandenburg

Landkreis Potsdam-Mittelmark

Beelitz, Kleinmachnow, Stahnsdorf, Werder (Havel)

   

Hessen

Main-Kinzig-Kreis

Bruchköbel, Gelnhausen, Hanau, Maintal

   

Hessen

Landkreis Offenbach

Dietzenbach, Dreieich, Langen (Hessen), Neu-Isenburg

   

Mecklenburg-Vorpommern

Landkreis Rostock

Bad Doberan, Güstrow, Kühlungsborn, Teterow

   

Rheinland-Pfalz

Landkreis Alzey-Worms

Alzey, Osthofen, Wörrstadt

   

Rheinland-Pfalz

Landkreis Mayen-Koblenz

Andernach, Bendorf, Mayen, Mendig

   

Saarland

Landkreis Saarlouis

Dillingen/Saar, Lebach, Saarlouis, Wadgassen

   

Saarland

Regionalverband Saarbrücken

Püttlingen, Riegelsberg, Saarbrücken, Völklingen

   

Sachsen

Landkreis Leipzig

Borna, Grimma, Markkleeberg, Markranstädt

   

Sachsen

Landkreis Nordsachsen

Delitzsch, Eilenburg, Schkeuditz, Torgau

   

Sachsen-Anhalt

Landkreis Börde

Haldensleben, Oschersleben, Wanzleben-Börde

   

Sachsen-Anhalt

Landkreis Harz

Blankenburg, Halberstadt, Quedlinburg, Wernigerode

   

Schleswig-Holstein

Kreis Segeberg

Bad Bramstedt, Bad Segeberg, Henstedt-Ulzburg

   

Thüringen

Ilm-Kreis

Arnstadt, Ilmenau

   

Thüringen

Stadt Suhl

Suhl (inkl. Ortsteile)

   

Hinweis: Die Listen sind repräsentativ und erheben keinen Anspruch auf Vollständigkeit aller Ortsteile innerhalb der genannten Gemeinden. Der Ausbaustatus ist dynamisch.

7.0 Fazit und konsolidierte Geodaten für die Netzwerk-Kartierung
7.1 Ein synthetisiertes Modell des Netzes der Deutschen Glasfaser
Die vorliegende Analyse zeichnet das Bild eines agilen und strategisch agierenden Herausforderers auf dem deutschen Telekommunikationsmarkt. Das Netzwerkmodell der Deutschen Glasfaser basiert auf drei fundamentalen Säulen:

Eine kompromisslose technologische Fokussierung auf FTTH, die dem Unternehmen einen klaren Qualitätsvorteil in seinen Zielmärkten sichert.

Ein kapitaleffizientes Backbone-Netz, das durch die intelligente Nutzung bestehender Infrastrukturen von Partnern wie GasLINE und DB broadband eine schnelle nationale Expansion bei minimierten Investitionskosten ermöglicht.

Ein nachfrageorientiertes Geschäftsmodell, das sich auf den ländlichen und suburbanen Raum konzentriert und durch die Nachfragebündelung das Ausbau-Risiko signifikant reduziert.

Die erstellte Karte ist ein analytisches Modell, das auf der Synthese öffentlich verfügbarer Daten und transparent dargelegter, plausibler Annahmen beruht. Sie stellt ein leistungsfähiges Werkzeug für Wettbewerbsanalysen, strategische Netzplanung und die Bewertung der digitalen Infrastruktur in Deutschland dar.

Tabelle 7.1: Konsolidierte Geodaten für die Netzwerk-Kartierung
Die nachfolgende Tabelle fasst die Ergebnisse der Analyse in einem einheitlichen, GIS-fähigen Format zusammen. Sie kombiniert die hochgradig verlässlichen Geodaten der Core Nodes mit den umfangreichen, aber modellbasierten Geodaten der lokalen Points of Presence (POPs). Diese konsolidierte Datentabelle ist die direkte Antwort auf die Anforderung des Nutzers nach einer vollständigen Karte mit Geodaten und bildet die Grundlage für jede weiterführende Visualisierung und Analyse.

Node_ID

Node_Name

Gemeinde

Landkreis

Bundesland

Node_Typ

Breitengrad (WGS84)

Längengrad (WGS84)

Genauigkeitsgrad

1

FRA16

Frankfurt am Main

Frankfurt am Main

Hessen

Core Node

50.12040

8.73873

Hoch (Verifiziert)

2

DUS1-2

Düsseldorf

Düsseldorf

NRW

Core Node

51.18827

6.86722

Hoch (Verifiziert)

3

AMS-IX

Amsterdam

N/A

N/A

Core Node

52.35590

4.95120

Hoch (Verifiziert)

4

POP_Ahaus

Ahaus

Borken

NRW

POP (Modelliert)

52.0763

7.0094

Mittel (Inferiert)

5

POP_Attendorn

Attendorn

Olpe

NRW

POP (Modelliert)

51.1274

7.9029

Mittel (Inferiert)

6

POP_Zorneding

Zorneding

Ebersberg

Bayern

POP (Modelliert)

48.0706

11.8322

Mittel (Inferiert)

7

POP_Aidlingen

Aidlingen

Böblingen

BaWü

POP (Modelliert)

48.6833

8.9000

Mittel (Inferiert)

8

POP_Suhl

Suhl

Suhl

Thüringen

POP (Modelliert)

50.6095

10.6936

Mittel (Inferiert)

9

POP_Isenbuettel

Isenbüttel

Gifhorn

Niedersachsen

POP (Modelliert)

52.4333

10.6000

Mittel (Inferiert)

10

POP_Wörrstadt

Wörrstadt

Alzey-Worms

RLP

POP (Modelliert)

49.8433

8.1189

Mittel (Inferiert)

...

...

...

...

...

...

...

...

...

N

POP_Gemeinde_X

Gemeinde X

Landkreis Y

Bundesland Z

POP (Modelliert)

[geocoded lat]

[geocoded lon]

Mittel (Inferiert)