Technische Spezifikation: Physikalische Schicht & Optische Parameter im DG-Netz
Dokument-Version: 1.0
Datum: 04. Juli 2025
Fokus: Detaillierte Analyse der physikalischen Komponenten, optischen Parameter und Berechnungsmodelle für die Signalübertragung und Dämpfung in einem FTTH-Netz der Deutschen Glasfaser.

1.0 Optische Sende- und Empfangsparameter (Transceiver)
Die Grundlage jeder optischen Übertragungsstrecke sind die aktiven Sende- und Empfangsmodule (Transceiver) im Optical Line Terminal (OLT) auf der Seite des Anbieters und im Optical Network Terminal (ONT) auf der Seite des Kunden.

1.1 PON-Technologien und Wellenlängenplan
Die Deutsche Glasfaser nutzt einen durchdachten Wellenlängenplan (Wavelength Division Multiplexing, WDM), um die Koexistenz verschiedener PON-Technologien auf einer einzigen Glasfaser zu ermöglichen. Dies ist der Schlüssel zur Zukunftssicherheit des Netzes.

Technologie

Richtung

Wellenlänge (nm)

Status im DG-Netz

Quelle

GPON (ITU-T G.984)

Downstream (OLT → ONT)

1490

Weit verbreitet (Bestandsnetz)

Upstream (ONT → OLT)

1310

Weit verbreitet (Bestandsnetz)

XGS-PON (ITU-T G.9807.1)

Downstream (OLT → ONT)

1577

Neuer Standard (seit 2024)

Upstream (ONT → OLT)

1270

Neuer Standard (seit 2024)


In Google Sheets exportieren
Die Nutzung unterschiedlicher Wellenlängenbänder stellt sicher, dass sich die Signale der verschiedenen Technologien nicht gegenseitig stören und ein Upgrade von GPON auf XGS-PON durch den reinen Tausch der Endgeräte möglich ist.

1.2 Leistungsklassen und Sende-/Empfangspegel
GPON-Equipment wird in optische Leistungsklassen eingeteilt, die das maximal tolerierbare Dämpfungsbudget einer Strecke definieren. Für Neuausbauten ist die Verwendung von leistungsfähigeren Klassen wahrscheinlich, um ausreichende Reserven zu schaffen.

Klasse

Max. Dämpfung

Typ. OLT Sendeleistung (Tx)

Typ. ONT Empfindlichkeit (Rx)

Status im DG-Netz

Quelle

Class B+

28 dB

+1,5 bis +5,0 dBm

-28 dBm

Etabliert

Class C+

32 dB

+3,0 bis +7,0 dBm

-30 dBm

Wahrscheinlich für Neuausbauten


In Google Sheets exportieren
OLT Sendeleistung (Transmit Power, Tx): Dies ist die optische Leistung, die das Sendemodul im PoP in die Faser einspeist. Ein typischer Wert für einen Class C+ Transceiver ist +5,0 dBm.

ONT Empfindlichkeit (Receiver Sensitivity, Rx): Dies ist die minimale optische Leistung, die am Empfangsmodul des Kunden-ONT ankommen muss, damit die Daten noch fehlerfrei gelesen werden können. Ein typischer Wert für einen empfindlichen Empfänger ist -30,0 dBm.

Verfügbares Gesamtbudget: Die Differenz zwischen der Sendeleistung des OLT und der minimalen Empfindlichkeit des ONT. Für eine Class C+ Verbindung ergibt sich daraus ein theoretisches Gesamtbudget von 35,0 dB (von +5 dBm auf -30 dBm). Dieses Budget wird durch die verschiedenen Dämpfungsfaktoren auf der Strecke "verbraucht".

2.0 Passive Komponenten und Dämpfungsfaktoren
Die gesamte Infrastruktur zwischen OLT und ONT ist im PON-Netz passiv, d.h., sie benötigt keinen Strom. Jede passive Komponente fügt dem Lichtsignal jedoch eine gewisse Dämpfung (Verlust) hinzu.

2.1 Glasfaser (Lichtwellenleiter)
Die Deutsche Glasfaser setzt auf moderne, biegeunempfindliche Singlemode-Glasfasern, um eine robuste und langlebige Installation zu gewährleisten.

Parameter

Wert

Anmerkungen

Quelle

Fasertyp

Singlemode, G.657.A2

Standard für FTTH, da sehr biegeunempfindlich, was die Installation in Gebäuden erleichtert.

Dämpfung bei 1310 nm

0,35 dB/km

Relevant für den Upstream (GPON).

Dämpfung bei 1490 nm

~0,35 - 0,4 dB/km

Relevant für den Downstream (GPON). Der Wert aus dem Dokument ist eine allgemeine Annahme.

Dämpfung bei 1550 nm

~0,25 dB/km

Relevant für optionale TV-Overlay-Dienste.

Dämpfung bei 1577 nm

~0,25 - 0,3 dB/km

Relevant für den Downstream (XGS-PON).


In Google Sheets exportieren
Die distanzabhängige Dämpfung ist ein linearer Faktor in der Budgetberechnung.

2.2 GPON-Splitter
Der passive optische Splitter ist das Herzstück der Punkt-zu-Mehrpunkt-Topologie. Er teilt das ankommende Downstream-Signal auf mehrere Kunden auf und bündelt die Upstream-Signale.

Parameter

Wert

Anmerkungen

Quelle

Typisches Split-Verhältnis

1:32

De-facto-Standard im DG-Netz. Bietet den besten Kompromiss aus Kosteneffizienz und Leistungsfähigkeit.

Technologie

PLC (Planar Lightwave Circuit)

Moderne Splitter-Technologie für gleichmäßige Aufteilung.

Typ. Einfügedämpfung (Insertion Loss)

-17,8 dB

Dies ist der größte einzelne Verlustfaktor im gesamten Leistungsbudget.


In Google Sheets exportieren
Obwohl Kaskadierungen (z.B. 1:8 gefolgt von 1:4) möglich sind, wird das Gesamtverhältnis von 1:32 in der Regel nicht überschritten.

2.3 Steckverbindungen (Konnektoren)
Jede lösbare Verbindung zwischen zwei Glasfasern wird über Stecker realisiert und fügt eine kleine Dämpfung hinzu.

Parameter

Wert

Anmerkungen

Quelle

Steckertyp

LC-APC, Grade B

Standard im FTTH-Bereich. Der "APC" (Angled Physical Contact) Schliff minimiert Rückreflexionen.

Typ. Einfügedämpfung (IL)

≤ 0,5 dB

Dieser Wert wird für jede einzelne Steckverbindung im Pfad angesetzt.


In Google Sheets exportieren
Ein typischer Pfad vom PoP zum Kunden hat mindestens vier Steckverbindungen:

Am ODF im PoP (Patchung zum Feeder-Kabel).

Am Eingang des NVt/DP (Feeder-Kabel zum Splitter-Eingang).

Am Ausgang des NVt/DP (Splitter-Ausgang zum Verteilkabel).

An der GF-TA in der Wohnung (Verbindung zum ONT-Patchkabel).

2.4 Spleiße (Schweißverbindungen)
Wo Fasern permanent miteinander verbunden werden (z.B. um längere Kabelstrecken zu realisieren), werden sie gespleißt (verschweißt).

Parameter

Wert

Anmerkungen

Quelle

Typ. Einfügedämpfung (IL)

~0,1 dB

Sehr geringer Verlust im Vergleich zu Steckern, aber auf langen Strecken relevant.


In Google Sheets exportieren
In einer Beispielrechnung wird von mindestens zwei Spleißen ausgegangen: einer im Feeder-Kabel und einer im Verteilkabel.

2.5 Wartungsmarge
Professionelle Netzplaner inkludieren eine pauschale Sicherheitsreserve, um unvorhergesehene Ereignisse und die Alterung von Komponenten über die Jahre abzufedern.

Parameter

Wert

Anmerkungen

Quelle

Typische Wartungsmarge

2,5 bis 3,0 dB

Diese Marge deckt zukünftige Reparaturen (die zusätzliche Spleiße erfordern), leichte Verschlechterung der Komponenten und Messungenauigkeiten ab.


In Google Sheets exportieren
(Ende von Teil 1. Der nächste Teil wird die vollständige Berechnung des Leistungsbudgets und die detaillierte Hierarchie der physischen Geräte im Zugangsnetz behandeln.)







weiter



Gedankengang anzeigen
Verstanden. Hier ist der zweite und letzte Teil des detaillierten technischen Dokuments zur physikalischen Schicht. Dieser Teil konzentriert sich auf die exakte Berechnung des Leistungsbudgets und die physische Hierarchie der Komponenten im Zugangsnetz.

3.0 Berechnung des optischen Leistungsbudgets (Optical Power Budget)
Das optische Leistungsbudget ist die zentrale Berechnung in der Planung und im Betrieb eines PON-Netzes. Sie bestimmt, ob ein Signal vom OLT den Kunden-ONT mit ausreichender Stärke erreicht. Die Berechnung ist eine einfache Summe aller Dämpfungsfaktoren entlang der Strecke, die von der Sendeleistung des OLT abgezogen wird.

3.1 Berechnungsformel
Die allgemeine Formel zur Berechnung der am ONT empfangenen Leistung lautet:

P 
Rx
​
 =P 
Tx
​
 −∑(IL 
Komponenten
​
 )

Wobei:

P 
Rx
​
  = Empfangene Leistung am ONT (in dBm)

P 
Tx
​
  = Sendeleistung des OLT (in dBm)

∑(IL 
Komponenten
​
 ) = Die Summe der Einfügedämpfungen (Insertion Loss) aller passiven Komponenten auf der Strecke (in dB).

Die detaillierte Formel für die Dämpfung lautet:

∑(IL)=IL 
Splitter
​
 +(L 
Faser
​
 ⋅IL 
Faser/km
​
 )+(N 
Stecker
​
 ⋅IL 
Stecker
​
 )+(N 
Spleiß
​
 ⋅IL 
Spleiß
​
 )+M 
Wartung
​
 

3.2 Beispielrechnung für eine typische DG-Strecke (Class C+)
Die folgende Tabelle zeigt eine beispielhafte, schrittweise Berechnung für eine typische GPON-Verbindung im Netz der Deutschen Glasfaser, basierend auf den Werten aus dem Analyse-Dokument. Sie verdeutlicht, wie die einzelnen Komponenten das Gesamtbudget beeinflussen.

#

Parameter / Komponente

Wert (dB/dBm)

Kumulativer Verlust (dB)

Anmerkungen

A

OLT Sendeleistung (Tx, Class C+)

+5,0 dBm

-

Startleistung, die in die Faser eingespeist wird.

B

ONT Empfindlichkeit (Rx, Min.)

-30,0 dBm

-

Minimal erforderliche Leistung am ONT.

C

Verfügbares Gesamtbudget (A - B)

35,0 dB

0,0

Die maximal tolerierbare Dämpfung auf der Strecke.

Verlustfaktoren auf der Strecke:

1

Verlust durch 1:32 Splitter

-17,8 dB

17,8

Größter einzelner Verlustfaktor. Typische Einfügedämpfung eines PLC-Splitters.

2

Verlust durch Steckverbindungen (4x)

-2,0 dB

19,8

Annahme: 4 Stecker (PoP, NVt-Eingang, NVt-Ausgang, GF-TA) mit je 0,5 dB Verlust.

3

Verlust durch Spleiße (2x)

-0,2 dB

20,0

Annahme: 1x im Feeder-, 1x im Verteilkabel mit je 0,1 dB Verlust.

4

Verlust durch Wartungsmarge

-3,0 dB

23,0

Eingeplante Sicherheitsreserve für Reparaturen, Alterung und Messungenauigkeiten.

D

Verbleibendes Budget für Faserstrecke (C - 1 - 2 - 3 - 4)

12,0 dB

35,0

Das Budget, das nach Abzug aller Fixverluste für die distanzabhängige Dämpfung der Glasfaser übrig bleibt.

E

Maximale Netzreichweite

~30 km

-

Kalkulation: 12,0 dB/0,4 dB/km. Dies liegt deutlich über der praktischen GPON-Grenze von 20 km und zeigt ein robustes Design.


In Google Sheets exportieren
Diese Berechnung demonstriert, dass die Architektur der DG mit einem 1:32-Split und Class-C+-Optiken über ein sehr robustes Leistungsbudget verfügt, das auch in ausgedehnten ländlichen Gebieten eine zuverlässige Verbindung sicherstellt.

4.0 Physische Hierarchie im Zugangsnetz (Netzebene 3 & 4)
Die folgende Sektion beschreibt die physischen Komponenten in der Reihenfolge, in der das Lichtsignal sie vom Point of Presence bis zum Kunden durchläuft.

4.1 Point of Presence (PoP)
Funktion: Der PoP ist das Herz des lokalen Netzes. Er ist eine aktive Vermittlungsstelle, die die Schnittstelle zwischen dem überregionalen Backbone und dem lokalen Zugangsnetz bildet.

Physische Merkmale: Meist ein vorgefertigtes, betoniertes Gebäude von der Größe einer Garage (z.B. 2,5m × 6,0m × 3,5m). Er erfordert eine redundante Stromversorgung, Klimatisierung und Sicherheitsmaßnahmen.

Interne Komponenten:

Optical Line Terminal (OLT): Das aktive Gerät, das die optischen Signale erzeugt und empfängt.

Optical Distribution Frame (ODF): Ein passives Gestellsystem (Glasfaser-Hauptverteiler), in dem die ankommenden Backbone-Fasern auf die abgehenden Feeder-Kabel zu den Netzverteilern aufgeteilt (rangiert) werden. Hier findet die erste Steckverbindung statt.

4.2 Netzverteiler (NVt) / Distribution Point (DP)
Funktion: Der NVt (auch DP genannt) ist der moderne Begriff für den grauen Kasten am Straßenrand. Er ist eine rein passive Komponente, deren einzige Funktion es ist, die ankommenden Fasern des Feeder-Kabels über Spleiße und den GPON-Splitter auf die kleineren Verteilkabel zu den Grundstücken zu verteilen.

Physische Merkmale: Die Gehäuse bestehen aus robusten Materialien wie glasfaserverstärktem Polycarbonat oder Aluminium und sind nach Schutzklassen wie IP55 zertifiziert. Sie sind modular und skalierbar, um dem Bedarf gerecht zu werden.

Modellserie (Beispiel)

Max. Spleißkapazität

Dimensionen (H x B x T in mm)

Quelle

CCM NVt 80

1.872

1455 x 750 x 310

Hexatronic NBD117102/24

648

858 x 425 x 300 (ohne Sockel)


In Google Sheets exportieren
4.3 Hausanschluss (Netzebene 4)
Die Installation innerhalb des Gebäudes folgt einem standardisierten Prozess mit klar definierten Komponenten.

Hausübergabepunkt (HÜP):

Funktion: Der passive Eintrittspunkt, an dem das von der Straße kommende Kabel im Gebäude endet (meist im Keller oder Hausanschlussraum). Er markiert den Übergang von Netzebene 3 zu Netzebene 4.

Physische Merkmale: Eine kleine, passive Anschlussbox mit typischen Maßen von ca. 16×9×3,5 cm.

Glasfaser-Teilnehmeranschluss (GF-TA):

Funktion: Die eigentliche Glasfaserdose in der Wohnung, vergleichbar mit einer Netzwerkdose. Sie wird mit dem HÜP über ein Glasfaser-Patchkabel verbunden (Länge bis 20m im EFH, bis 30m im MFH).

Physische Merkmale: Eine Anschlussdose mit einer LC-APC-Schnittstelle, an die der ONT angeschlossen wird. Hier findet die letzte Steckverbindung im Pfad statt.

Optical Network Terminal (ONT) / Netzabschluss (NT):

Funktion: Das aktive Gerät, das das ankommende Lichtsignal in ein elektrisches Ethernet-Signal für den Kundenrouter umwandelt. Es ist die letzte Komponente, die zur Infrastruktur der DG gehört und wird per OMCI ferngewartet.

Physische Merkmale: Ein Wandgerät, das eine 230V-Steckdose benötigt und per RJ45-Kabel mit dem Router verbunden wird.