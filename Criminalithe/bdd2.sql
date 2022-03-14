BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "source" (
	"source_id"	INTEGER NOT NULL,
	"source_date"	INTEGER,
	PRIMARY KEY("source_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "user" (
	"user_id"	INTEGER,
	"user_nom"	TEXT,
	"user_login"	TEXT,
	"user_email"	TEXT,
	"user_password"	TEXT,
	PRIMARY KEY("user_id")
);
CREATE TABLE IF NOT EXISTS "authorship" (
	"authorship_id"	INTEGER NOT NULL,
	"authorship_amendes_id"	INTEGER,
	"authorship_user_id"	INTEGER NOT NULL,
	"authorship_date"	DATETIME,
	"authorship_personnes_id"	INTEGER,
	"authorship_source_id"	INTEGER,
	PRIMARY KEY("authorship_id" AUTOINCREMENT),
	FOREIGN KEY("authorship_amendes_id") REFERENCES "amendes"("amendes_id"),
	FOREIGN KEY("authorship_source_id") REFERENCES "source"("source_id"),
	FOREIGN KEY("authorship_user_id") REFERENCES "authorship",
	FOREIGN KEY("authorship_personnes_id") REFERENCES "personnes"("personnes_id")
);
CREATE TABLE IF NOT EXISTS "personnes" (
	"personnes_id"	INTEGER NOT NULL,
	"personnes_amendes_id"	INTEGER,
	"personnes_nom"	TEXT,
	"personnes_prenom"	TEXT,
	PRIMARY KEY("personnes_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "amendes" (
	"amendes_id"	INTEGER NOT NULL,
	"amendes_source_id"	INTEGER,
	"amendes_montant"	INTEGER,
	"amendes_type"	TEXT,
	"amendes_franche_verite"	TEXT,
	"amendes_transcription"	TEXT,
	"amendes_personnes_id"	INTEGER,
	PRIMARY KEY("amendes_id" AUTOINCREMENT),
	FOREIGN KEY("amendes_source_id") REFERENCES "source"("source_id")
);
INSERT INTO "source" VALUES (6234,1430);
INSERT INTO "source" VALUES (6235,1430);
INSERT INTO "source" VALUES (6236,1431);
INSERT INTO "source" VALUES (6237,1431);
INSERT INTO "source" VALUES (6238,1432);
INSERT INTO "source" VALUES (6239,1432);
INSERT INTO "source" VALUES (6240,1433);
INSERT INTO "source" VALUES (6241,1433);
INSERT INTO "source" VALUES (6242,1434);
INSERT INTO "source" VALUES (6243,1434);
INSERT INTO "user" VALUES (1,'decraene','valentin','valentin.de.craene@hotmail.fr','pbkdf2:sha256:260000$8M3M50H5t5i92JcX$fb6ced6a9183f4fbede99fecd60f48d57a53b22b1bcedbd5da215a69cf1f0268');
INSERT INTO "user" VALUES (2,'de_craene','valentdeux','valentin.de.craene@chartes.psl.eu','pbkdf2:sha256:260000$mo1gvkGuE563dizM$9ea508dddfeee58091a21bd9c9f137e7af4086ec529ede3bb54fac2db5b44639');
INSERT INTO "authorship" VALUES (1,1,1,'2022-02-17 14:57:16.326086',NULL,NULL);
INSERT INTO "authorship" VALUES (2,1,1,'2022-02-17 14:57:21.448883',NULL,NULL);
INSERT INTO "personnes" VALUES (1,1,'Desmasieres','Enrardin');
INSERT INTO "personnes" VALUES (2,2,'Rameri dit de Boulogne','Simonet');
INSERT INTO "personnes" VALUES (3,3,'Le Noir de Quesnoit','Jacquement');
INSERT INTO "personnes" VALUES (4,4,'Angouart','Estienne');
INSERT INTO "personnes" VALUES (5,5,'de Wagnon','Hanequin');
INSERT INTO "personnes" VALUES (6,6,'de Boulogne','Jacot');
INSERT INTO "personnes" VALUES (7,7,'de Wudumgehem','Rolland');
INSERT INTO "personnes" VALUES (8,8,'Duhem','Bernard');
INSERT INTO "personnes" VALUES (9,9,'le Blont','Hanequin');
INSERT INTO "personnes" VALUES (10,10,'Leman','Jacquement');
INSERT INTO "personnes" VALUES (11,11,'Prevost','Hanequin');
INSERT INTO "personnes" VALUES (12,12,'de Mulencourt','Pierot');
INSERT INTO "personnes" VALUES (13,13,'Lefeuve','Simonnet');
INSERT INTO "personnes" VALUES (14,14,'de la Montaigne','Jehan');
INSERT INTO "personnes" VALUES (15,15,'du Thoit','Jehan');
INSERT INTO "personnes" VALUES (16,16,'de Lannoit','Helloi');
INSERT INTO "personnes" VALUES (17,17,'de Molin','Colart');
INSERT INTO "personnes" VALUES (18,18,'Varat','Jeannot');
INSERT INTO "personnes" VALUES (19,19,'Belhome','Vandart');
INSERT INTO "personnes" VALUES (20,20,'Pulsier','Jehan');
INSERT INTO "personnes" VALUES (21,21,'de Haquegnies','Gérard');
INSERT INTO "personnes" VALUES (22,22,'Le Noir','Jacquement');
INSERT INTO "personnes" VALUES (23,23,'Wicart','Robin');
INSERT INTO "personnes" VALUES (24,24,'Despieres','Jehan');
INSERT INTO "personnes" VALUES (25,25,'Poullart','Jehan');
INSERT INTO "personnes" VALUES (26,26,'Bachelier','Gillart');
INSERT INTO "personnes" VALUES (27,27,'Renare','Gillart');
INSERT INTO "personnes" VALUES (28,28,'Aloe','Pasquier');
INSERT INTO "personnes" VALUES (29,29,'Renier','Jacquement');
INSERT INTO "personnes" VALUES (30,30,'Tenelin','Robert');
INSERT INTO "personnes" VALUES (31,31,'d Orchies','Helloi');
INSERT INTO "personnes" VALUES (32,32,'de Levincourt','Vivain');
INSERT INTO "personnes" VALUES (33,33,'Du Patui','Fremin');
INSERT INTO "personnes" VALUES (34,34,'Lemaistre','Pierre');
INSERT INTO "personnes" VALUES (35,35,'de le Val','Massui');
INSERT INTO "personnes" VALUES (36,36,'Bonnier','Daniel');
INSERT INTO "personnes" VALUES (37,37,'de Berck','Girardin');
INSERT INTO "personnes" VALUES (38,38,'de Callonne','Jehan');
INSERT INTO "personnes" VALUES (39,39,'Vignon dit de Bondues','Quentin');
INSERT INTO "personnes" VALUES (40,40,'Leuridan','Gillart');
INSERT INTO "personnes" VALUES (41,41,'Condewan','Robert');
INSERT INTO "personnes" VALUES (42,42,'Brehart','Hanequin');
INSERT INTO "personnes" VALUES (43,43,'Vilette','Helbert');
INSERT INTO "personnes" VALUES (44,44,'le Mannier','Hanequin');
INSERT INTO "personnes" VALUES (45,45,'le Blancq','Jacot');
INSERT INTO "personnes" VALUES (46,46,'de Bours','Jehan');
INSERT INTO "personnes" VALUES (47,47,'Carette','Pieronnelle');
INSERT INTO "personnes" VALUES (48,48,'du Hem','Jehan');
INSERT INTO "personnes" VALUES (49,49,'de le Montaigne','Marquet');
INSERT INTO "personnes" VALUES (50,50,'Briquemart','Alard');
INSERT INTO "personnes" VALUES (51,51,'Deffontaines','Gillot');
INSERT INTO "personnes" VALUES (52,52,'du Rieu','Jehan');
INSERT INTO "personnes" VALUES (53,53,'de la Masure','Hanequin');
INSERT INTO "personnes" VALUES (54,54,'de la Vallée','Robert');
INSERT INTO "personnes" VALUES (55,55,'Lauwe','Jacot');
INSERT INTO "personnes" VALUES (56,56,'Carpentier','Pierre');
INSERT INTO "personnes" VALUES (57,57,'le Leu','Jehan');
INSERT INTO "personnes" VALUES (58,58,'Descamp','Benoit');
INSERT INTO "personnes" VALUES (59,59,'du Castel','Martinet');
INSERT INTO "personnes" VALUES (60,60,'de Premecque','Guillaume');
INSERT INTO "personnes" VALUES (61,61,'Morel','Caisin');
INSERT INTO "personnes" VALUES (62,62,'le Trehent','Mahieu');
INSERT INTO "personnes" VALUES (63,63,'Denis','Jacquement');
INSERT INTO "personnes" VALUES (64,64,'Agache de Flers','Jacquement');
INSERT INTO "personnes" VALUES (65,65,'Fremault','Parposie');
INSERT INTO "personnes" VALUES (66,66,'du Hem','Jacquement');
INSERT INTO "personnes" VALUES (67,67,'Foubert','Jacquement');
INSERT INTO "personnes" VALUES (68,68,'du Sautoir','Jehan');
INSERT INTO "personnes" VALUES (69,69,'Villette','Jehan');
INSERT INTO "personnes" VALUES (70,70,'de Premecque','Jacques');
INSERT INTO "personnes" VALUES (71,71,'Desambris','Pierre');
INSERT INTO "personnes" VALUES (72,72,'le Noir','Jacques');
INSERT INTO "personnes" VALUES (73,73,'de Brabant','Jacquement');
INSERT INTO "personnes" VALUES (74,74,'Lansel','Hanequin');
INSERT INTO "personnes" VALUES (75,75,'Cordewanier','Robert');
INSERT INTO "personnes" VALUES (76,76,'Merchant','Jehan');
INSERT INTO "personnes" VALUES (77,77,'de Quesne','Bastard');
INSERT INTO "personnes" VALUES (78,78,'de Quesne','Bastard');
INSERT INTO "personnes" VALUES (79,79,'Pardon','Jehan');
INSERT INTO "personnes" VALUES (80,80,'Espinette','Michel');
INSERT INTO "personnes" VALUES (81,81,'de Lattue dit Destrassielles','Jehan');
INSERT INTO "personnes" VALUES (82,82,'du Tertre','Jehan');
INSERT INTO "personnes" VALUES (83,83,'du Thoit','Jacquement');
INSERT INTO "personnes" VALUES (84,84,'de la Deulle','Jehan');
INSERT INTO "personnes" VALUES (85,85,'Tencart','Henry');
INSERT INTO "personnes" VALUES (86,86,'de Candele','Jehan');
INSERT INTO "personnes" VALUES (87,87,'Lors','Bertrand');
INSERT INTO "personnes" VALUES (88,88,'Blancart','Pierre');
INSERT INTO "personnes" VALUES (89,89,'Brediere','Jehan');
INSERT INTO "personnes" VALUES (90,90,'Doremieux','Girard');
INSERT INTO "personnes" VALUES (91,91,'de la Vallée','Jehan');
INSERT INTO "personnes" VALUES (92,92,'Thomart','Jehan');
INSERT INTO "personnes" VALUES (93,93,'de Laval','Willot');
INSERT INTO "personnes" VALUES (94,94,'Lambelin','Jehan');
INSERT INTO "personnes" VALUES (95,95,'du Mortier','Jacquement');
INSERT INTO "personnes" VALUES (96,96,'le Blocq','Pierot');
INSERT INTO "personnes" VALUES (97,97,'de Langle','Pierre');
INSERT INTO "personnes" VALUES (98,98,'le Blancs','Jehan');
INSERT INTO "personnes" VALUES (99,99,'Bonnier','Karesnne');
INSERT INTO "personnes" VALUES (100,100,'du Prêt','Martin');
INSERT INTO "personnes" VALUES (101,101,'le Mire','Ansel');
INSERT INTO "amendes" VALUES (1,6234,60,'vol','non','Pour avoir pris et emporté certaines cloyes appartenant à aultruy receu LX sous',1);
INSERT INTO "amendes" VALUES (2,6234,40,'port_arme','non','saisis d''une matraque cerstellée et pour ce ainsi qu il avoit defailli de comparaitre par devant ledit bailli, receu XL sous',2);
INSERT INTO "amendes" VALUES (3,6234,80,'violence_physique','non','en nom de Hanequin le Maistre qui avoit batu et manié es mettes dudit bailliage le mesquirre de Hanequin de Lomme, receu IIII livres',3);
INSERT INTO "amendes" VALUES (4,6234,60,'violence_physique','non','pour et nom de Loycquin Destembrughe serviteur de Gerard de Houpplines qui avoit esté present es mettres dudit bailliage saisi donné matraque esteller receu LX sous',4);
INSERT INTO "amendes" VALUES (5,6234,20,'port_arme','non','presens et arrester pour cause que es mettes dudit bailliage il fut trouver saisi dun becq de faucon appointé, receu XX sous',5);
INSERT INTO "amendes" VALUES (6,6234,80,'violence_physique','non','souppechonez d''avoir batu en dit bailliage une nommé Jehan Franquart et icelle ribée contre son gré receu IIII livres',6);
INSERT INTO "amendes" VALUES (7,6234,60,'violence_physique','non','en nom de Colart de Casan qui avoit batu et manié en dit bailliage ung nommé Jacquement Cousturier en layde dautruis autres ses compliches receu LX sous',7);
INSERT INTO "amendes" VALUES (8,6234,20,'port_arme','oui','pour cause qu il es franques vertitez de mon dit seigneur tennés en l''an XXVII a Englos il avoit esté pourtrais d''avoir porté en dit bailliage arme nues deffendues receu XX sous',8);
INSERT INTO "amendes" VALUES (9,6234,60,'port_arme','oui','pour cause que es franques vertiez de mon dit seingeur teneues en l an mil IIII c XXIIII a Esquerme il avoit esté pourtrais d avoir en dit bailliage porté armes nues deffendues receu LX sous',9);
INSERT INTO "amendes" VALUES (10,6234,20,'port_arme','non','saisi d''armes nues deffendues receu par appointement en consideracion a la requeste que en fist Blankart Desprez escuier receu XX sous',10);
INSERT INTO "amendes" VALUES (11,6234,20,'port_arme','oui','franques veritez de mon dit seigneur tenues en l an mil IIII c XXIIII il avoit esté pourtrais d''avoir en dit bailliage porté armes nues appointé en faveur qu il esté a Baudi de Lannoy receu XX sous',11);
INSERT INTO "amendes" VALUES (12,6235,20,'violence_physique','non','souppechonné d''avoir batu et manié es mettes dudit bailliage ung nommé Hacot du Hem',12);
INSERT INTO "amendes" VALUES (13,6235,20,'désobéissance','non','avoit desobey aux sergens du dit bailliage en l''un d''eulx receu XX sous',13);
INSERT INTO "amendes" VALUES (14,6235,20,'brigandage','non','souppechonné davoir ou dit bailliage fait ou fait faire assembler une compaigne de guerre a l''encontre d aultruy receu XX sous',14);
INSERT INTO "amendes" VALUES (15,6235,33,'port_arme','oui','rapport de franques verités tenues en l''an XXVI il estoit pourtrés d avoir en dit bailliage porté arme nues deffendues receu XXXIII sous',15);
INSERT INTO "amendes" VALUES (16,6235,60,'violence_physique','non','pour avoir batu manié es mettes dudit bailliage ung nommé Jacot le Semerre receu LX sous',16);
INSERT INTO "amendes" VALUES (17,6235,20,'port_arme','oui','rapporté de franques verites tenues en l an XVIII d avoir au dit bailliage porté armes nues deffendues receu XX sous',17);
INSERT INTO "amendes" VALUES (18,6235,60,'port_arme','non','pour cause que en dit bailliage il fu trouvés saisis d''un arcq a main et de six fleches receu XL sous',18);
INSERT INTO "amendes" VALUES (19,6235,60,'port_arme','oui','rapporté par franqaues verités tenues en l'' an XXVI d avoir en dit bailliage porté arme nues deffendues receu LX sous',19);
INSERT INTO "amendes" VALUES (20,6235,60,'port_arme','oui','pour semblable rapport de verités d''avoir ou dit bailliage porté arme nues deffendues receu LX sous',20);
INSERT INTO "amendes" VALUES (21,6235,26,'port_arme','non','presens et arresté en dit bailliage saisi d'' une macque certellée appointé receu XXVI sous',21);
INSERT INTO "amendes" VALUES (22,6235,60,'violence_physique','non','qui avoit batu et manié es mettes dudit bailliage la femme de Mahieu Desrumaulx receu LX sous',22);
INSERT INTO "amendes" VALUES (23,6236,80,'vol','non','esté pris saisi d une hache d'' armes et pour ce aussi quil avoit defailli de comparoir devant le bailli receu IIII livres',23);
INSERT INTO "amendes" VALUES (24,6236,60,'vol','non','pour et en l''acquit de Jehan Haquelotte qui avoit pris et emporté certain tonlieu deu a monseigneur le duc et ce oultre le gré et voulenté du fermier de mon dit seigneur receu LX sous',24);
INSERT INTO "amendes" VALUES (25,6236,60,'tapage_nocturne','non','souppechonné d''avoir conssomé et repaieyé de nuyt en lostel dun nommé Le Grand Gillart et ce oultre le gré et volenté dudit Gillart receu LX sous',25);
INSERT INTO "amendes" VALUES (26,6236,80,'rapt','non','souppechonné  d'' avoir avecq lui emené Katerine Flamencq femme Mahieu Ronscé receu IIII livres',26);
INSERT INTO "amendes" VALUES (27,6236,60,'défaut_comparution','oui','deffailli de venir a certaine veritez tenues a Frelenghien par enseignement de loy receu LX sous',27);
INSERT INTO "amendes" VALUES (28,6236,60,'défaut_comparution','oui','deffailli de venir a certaine veritez tenues a Frelenghien par enseignement de loy receu LX sous',28);
INSERT INTO "amendes" VALUES (29,6236,60,'défaut_comparution','oui','deffailli de venir a certaine veritez tenues a Frelenghien par enseignement de loy receu LX sous',29);
INSERT INTO "amendes" VALUES (30,6236,60,'défaut_entretien','non','en quy par le jugement et enseignement des hommes de fief de la Salle de Lille avoit esté condepuez pour faultre de reparacion chemin trouvée contre son heritage receu LX sous',30);
INSERT INTO "amendes" VALUES (31,6236,28,'défaut_entretien','non','pour cause que contre son heritage on avoit trouvé plusieurs deffaultes de reparacion de chemin receu XXVIII sous',31);
INSERT INTO "amendes" VALUES (32,6236,20,'brigandage','non','souppechoné d''avoir fouy et entrepris sur le grand chemin de Douay receu XX sous',32);
INSERT INTO "amendes" VALUES (33,6237,20,'vol','non','souppechonné d''avoir pris et emporté une planque qui estoit es marez de Barghes receu XX sous',33);
INSERT INTO "amendes" VALUES (34,6237,26,'défaut_main_justice','non','auquel on jusposoit avoir enfraint la main de justice qui mise et assize avoit esté a ung bosquet appartenant a Jehan de Pues receu XXVI sous',34);
INSERT INTO "amendes" VALUES (35,6237,20,'violence_physique','non','souppechonnez d'' avoir batu et manié es mettes du dit bailliage ung nommé Jacquement de Beaumore receu XX sous',35);
INSERT INTO "amendes" VALUES (36,6237,60,'violence_physique','oui','pour cause qu il avoit desobbey aux sergens dudit bailliage qui par rapport de franques vertitez et pour aultre jeu aux dez le avoient pris et arresté au dit lieu de Bondred recey LX sous',36);
INSERT INTO "amendes" VALUES (37,6237,66,'port_arme','non','pour et en l'' acquit de Pierot de Sernay et Gillot Deswastuées qui par Percheval Flamencq sergent dudit bailli avoit esté punis saisi d armes nues deffendues et de trait es mettes dicelluy bailliage receu LXVI sous',37);
INSERT INTO "amendes" VALUES (38,6237,26,'port_arme','non','pour et en l'' acquit de Pierot le Foulon qui par Watier de Courchelles sergens dudit bailli avoit esté presens es mettes dicellui bailli saisi d une burghemart receu XXVI sous',38);
INSERT INTO "amendes" VALUES (39,6237,60,'violence_physique','non','qui avoit esté mis prsonnier a cause que es mettes dudit bailliage il avoit batu et manié le berguier Mahieu le Bay receu LX sous',39);
INSERT INTO "amendes" VALUES (40,6237,60,'défaut_entretien','non','pour et en nom des hoirs de Regnault Desprez qui par les hommes de fief de la Salle de Lille au convienment dudit bailli avoit esté demipriez pour faulte de reparacion de chemin trouvée en leur heritage receu LX sous',40);
INSERT INTO "amendes" VALUES (41,6237,60,'port_arme','non','pour et en l'' acquit de Piere Domessent pour cause qu il avoit esté pris es mettes dudit bailliage saisi d armes nues deffendues receu LX sous',41);
INSERT INTO "amendes" VALUES (42,6237,60,'dégradation','non','pour et en l'' acquit de Mestmette sa fille qui avoit esté prise pour cause qu elle estoit souppechonnée d avoir coppé les renes de une barque et un bonnel appartenans a Jacquemant Bonrard',42);
INSERT INTO "amendes" VALUES (43,6238,60,'défaut_entretien','non','avoit esté condempnez par lesdits hommes de fiefs au dit convienment pour deffaultre de reparacion de chemin trouvé contre son heritage receu LX sous',43);
INSERT INTO "amendes" VALUES (44,6238,26,'port_arme','oui','avoit esté rapportez et pourtrais es franques veritez de mon dit seigneur le duc d'' avoir en dit bailliage porté armes nues deffendues receu XXVI sous',44);
INSERT INTO "amendes" VALUES (45,6238,60,'port_arme','non','pris par Gillet de la Vallée sergent dudit bailliage de Lille, pour cause qu il s'' estoit resceux hors des mains de Huart de la Ruelle sergens de la dame d Anerchin qui sur la terre et seignoirie d icelle li avait pris saisi d'' armes nues deffendues receu LX sous',45);
INSERT INTO "amendes" VALUES (46,6238,60,'défaut_entretien','non','pour et en l'' acquit de Alard le veuf qui par les hommes de fief de la Salle de Lille au convienement dudit bailli avoit esté condempuez pour faultre de reparacion de chemin trouvée en son heritage receu LX sous',46);
INSERT INTO "amendes" VALUES (47,6238,60,'défaut_main_justice','non','pour cause que en enfraignant la main de justice elle avoit de fait emmené certain mombre de veste acorné appartenant a Regault Prenest et lesqeulles avoient esté prises en dommage d'' aultrui par le sergent du seigneur du fief de le Warwane receu LX sous',47);
INSERT INTO "amendes" VALUES (48,6238,60,'port_arme','oui','rapport de franques veritez darranierement tenues a Haluin avoit esté pourtrais d avoir en dit bailllliage porté armes nues deffendues receu LX sous',48);
INSERT INTO "amendes" VALUES (49,6238,60,'port_arme','non','pour cause de ce qu il avoit esté pris pour le port de ses armes nues deffendues et qu'' il avoit defalli de comparoir pardevant le dit bailli receu LX sous',49);
INSERT INTO "amendes" VALUES (50,6238,60,'défaut_entretien','non','par le jugement des hommes de fief de la salle de Lille au convienment dudit bailli il avoit esté condempuez pour deffaultre de reparacion de chemin trouvé contre son heritage receu LX sous',50);
INSERT INTO "amendes" VALUES (51,6238,60,'vol','non','condempue par lesdit hommes de la Sale au convienment dudit bailli pour faulte de reparacion de fossé trouvée contre son heritage qu'' il a Bourghelle receu LX sous',51);
INSERT INTO "amendes" VALUES (52,6238,60,'violence_physique','non','pour causse que on lui supposoit avoir  fourmené et rivé Miquelette Lenchon et niepce d icelle aultre leur gré',52);
INSERT INTO "amendes" VALUES (53,6239,80,'soutien_banni','non','pour et en nom d'' Estene son filz qui estoit souppechonnez et renommez d'' avoir soustoité en son hostel pour plusieurs fois ung nommé Guillebert Grinmelin estant bany du pays et conté de Flandre receu IIII livres',53);
INSERT INTO "amendes" VALUES (54,6239,60,'violence_physique','non','en la paroice de Lomme sous le dit bailliage de Lille il avoit batu et manié ou fait batre et manier ung nommé Haquinet Wagnon receu LX sous',54);
INSERT INTO "amendes" VALUES (55,6239,60,'vol','non','pour cause que eulz et autres leurs complices avoient de fait assembler et a main armée pris et emporté ung caudron et une quesne d'' estain qui lors estoit sequestrée et mise en l ostel de Jehan Follet a Merigmes receu LX sous',55);
INSERT INTO "amendes" VALUES (56,6239,60,'violence_physique','non','pour et en nom de Mahieu le Leu son frere qui avoit batu et manié es mettes dudit bailliage une femme nommée Ichenne Descamps receu LX sous',56);
INSERT INTO "amendes" VALUES (57,6239,60,'violence_physique','non','souppechonné d''avoir en enfraingant paix feun par ire d un baston sur ung nommé Ichene Destailleurs receu LX sous',57);
INSERT INTO "amendes" VALUES (58,6239,60,'violence_physique','non','pour cause qu'' il avoit aucunnement manié ou rivé la fille Noel de la Salle et ce oultre le gré d icelle receu LX sous',58);
INSERT INTO "amendes" VALUES (59,6239,80,'vol','non','pour et en nom de Lotard du Hem qui estoit rennomez d'' avoir environ a XIIII ans pris ung laron qui larchenieusement emportoit garbes de bled appartenant au père dudit Lotard du Hem et que pour argent ou aultrement de sa voulente il avoit deluivré ledit laron sans le mettre es mains de justiche receu IIII livres',59);
INSERT INTO "amendes" VALUES (60,6239,60,'dégradation','non','pour cause qu'' il avoit entré en l'' ostel de Hustin de le Flamengerne et en icelluy hostel tue aucuns des cauchons du dit Hustin et ce oultre son gré receu LX sous',60);
INSERT INTO "amendes" VALUES (61,6239,26,'port_arme','non','pour cause qu'' il avoit defalli de comparoir a certain jour a lui assigné après qu'' il eubt esté pris saisi d armes nues deffendues receu XXVI sous',61);
INSERT INTO "amendes" VALUES (62,6239,60,'défaut_main_justice','non','pour et en nom de Hanequin Tonnel son varlet qu'' il avoit pris et emporté en lostel dudit de lespiere certains bien qui avoient sur lheritage d'' icellui de Lespiere et lesquelx bien estoient lors saisi et mis en main de justiche receu LX sous',62);
INSERT INTO "amendes" VALUES (63,6240,60,'violence_physique','non','pour cause qu'' il avoit batu et manié es mettes dudit bailliage et de trait ung nommé Baudechon Cloquier receu LX sous',63);
INSERT INTO "amendes" VALUES (64,6240,60,'vol','non','pour et en nom de Jacot son bregier qui de fait et puissance avoit rescoux les brebis de son dit maistre qui en dommage d aultrui avoit esté prises par Jehan Blancart sergent messier  en l'' escheviange d'' Anappe receu LX sous',64);
INSERT INTO "amendes" VALUES (65,6240,26,'violence_physique','non','pour et en l'' acquit de Hanequin Robiquet qui esté souppechonnéz d'' avoir batu et mané es mettes dudit bailliage Hanequin Fremault receu XXVI sous',65);
INSERT INTO "amendes" VALUES (66,6240,60,'défaut_entretien','non','par le jugement des hommes de fief de la Salle de Lille au convienment dudit bailli il avoit esté condempnez pour faultre de reparacion de chemin trouvée contre son heritage receu LX sous',66);
INSERT INTO "amendes" VALUES (67,6240,60,'port_arme','oui','es franques veritez de mon dit seigneur tenues en l'' an 1421 a Phalempin il avoit esté pourtrais davoir en dit bailliage porté armes nues deffendues',67);
INSERT INTO "amendes" VALUES (68,6240,60,'défaut_entretien','non','en nom de Piere d'' Autreulles escuier en quoy par les hommes de fiefs il avoit esté condempnez pour faultre de reparacion de chemin trouvé receu LX sous',68);
INSERT INTO "amendes" VALUES (69,6240,60,'défaut_entretien','non','pour et en lacquit de Jehan et Aleaermet Rousée freres pour semblable receu LX sous',69);
INSERT INTO "amendes" VALUES (70,6240,60,'violence_physique','non','pour eulz et leurs complices souppechonnez d'' avoir batu et manié es mettes dudit bailliage Mahieu Castel receu LX sous',70);
INSERT INTO "amendes" VALUES (71,6240,60,'vol','non','pour cause qu il avoit fait deshaner certaines cloches sur l'' héritage des relligieuses des prez de Tournay estant a Grinisons receu LX sous',71);
INSERT INTO "amendes" VALUES (72,6240,60,'défaut_entretien','non','en l'' acquit de Jehan Cappel qui par les hommes de fief avoit esté condempnez pour faultre de reparacion de chemin trouvée contre son heritage qu'' il a construit assez prez de Perenchies receu LX sous',72);
INSERT INTO "amendes" VALUES (73,6241,60,'violence_physique','non','pris et arresté es mettes dudit bailliage pour cause que en iccelui il avoit batu et manié Hugue d'' Avelang receu LX sous',73);
INSERT INTO "amendes" VALUES (74,6241,26,'port_arme','oui','par franques veritez tenues en l'' an mil quatre cent vingt et ung en la paroice de Templeuve en Pevele il avoit esté rapportéz d avoir en dit bailliage porté armes nues deffendues et pour ce aussi que on lui juiposoit avoir batu en dit bailliage ung compaignon receu XXVI sous',74);
INSERT INTO "amendes" VALUES (75,6241,60,'vol','non','pour et en nom de Jehan de Queumille dit le Loncq pour cause quon lui juiposoit avoir pris ung francart appartenant a Rolland de Wartembecuqe le Fouvrelle receu LX sous',75);
INSERT INTO "amendes" VALUES (76,6241,60,'port_arme','non','pour et en l'' acquit de Hanequin Roussel qui avoit esté pris es mettes dudit bailliage saisi d'' une macque trestelcé receu LX sous',76);
INSERT INTO "amendes" VALUES (77,6241,60,'port_arme','non','pour et en nom de Colart Traspournant qui pareillement avoit esté pris en dit bailliage saisi d'' une macque trestelcé receu LX sous',77);
INSERT INTO "amendes" VALUES (78,6241,26,'violence_physique','non','pour et en lacquit de Bonrard de le Croix pour cause quil estoit rennoméz d'' avoir batu et manié es mettes dudit bailliage ung nommé Jacquemont Hallet receu XXVI sous',78);
INSERT INTO "amendes" VALUES (79,6241,26,'défaut_entretien','non','et autres tuteurs et curateurs des enfans Menuedans feu Jehan de Motte en quoy par les hommes de fief  ils avoient esté condempneé pour faulte de reparacion de chemin trouvée contre leur heritage receu XXVI sous',79);
INSERT INTO "amendes" VALUES (80,6241,60,'brigandage','non','pour cause quil avoit foui et entrepris avec autres sur l'' heritage es regez de mon dit seigneur en hamel d Anequin receu LX sous',80);
INSERT INTO "amendes" VALUES (81,6241,26,'port_arme','non','pour cause qu il avoit esté pris es mettes dudit bailliage saisi d'' armes nues deffendues receu XXVI sous',81);
INSERT INTO "amendes" VALUES (82,6241,26,'violence_physique','non','estoit souppechonnez d'' avoir batu et manié la femme du ladre de Wanebrechies',82);
INSERT INTO "amendes" VALUES (83,6242,60,'défaut_entretien','non','par le jugement des hommes de fief de la Salle de Lille au convienment dudit bailli il avoit esté condempnez pour faulte de reparacion de chemin trouvée contre son heritage receu LX sous',83);
INSERT INTO "amendes" VALUES (84,6242,80,'violence_physique','non','qu'' il avoit manié et ribé Colle Crombet femme et espouse de Grard le Peskeur oultre le gré d icelle receu IIII livres',84);
INSERT INTO "amendes" VALUES (85,6242,60,'violence_physique','non','pour cause qu'' il avoit batu et amnié es mettes dudit bailliage Estenet Bonnehemie receu LX sous',85);
INSERT INTO "amendes" VALUES (86,6242,60,'défaut_entretien','non','esté condempnez pour faultre de reparacion de fossé et chemin trouvée contre son heritage a Semonielle',86);
INSERT INTO "amendes" VALUES (87,6242,80,'vol','non','pris et arresté es mettes dudit bailliage pour cause que on lui juiposoit avoir emporté certain nombre de garbes de bled a Mathieu Vandoul et pour avoir entré en la chambre dudit Mahieu oultre son gré et aussi pour le port d une marque certellée receu IIII livres',87);
INSERT INTO "amendes" VALUES (88,6242,60,'violence_physique','non','pour et en nom de Hanequin son filz pour cause qu'' il avoit batu et manié es mettes dudit bailliage le Bregier Jehan Fremin receu LX sous',88);
INSERT INTO "amendes" VALUES (89,6242,160,'conflit_juridiction','non','pour et en nom des bailli ou keurte et eshcevins des religieux de Saint Quentin en Iller ausquelz ledit bailli leur juiposoit avoir mespris en fait des loys receu VIII livres',89);
INSERT INTO "amendes" VALUES (90,6242,60,'défaut_entretien','non','avoit esté condempnez pour faulte de reparacion de chemin trouvée contre son heritage receu LX sous',90);
INSERT INTO "amendes" VALUES (91,6242,60,'violence_physique','non','pour et en lacquit de Hostelet Carette qui avoit esté pris pour cause que lui juiposoit avoir batu et manié es mettes dudit bailliage ung nommé Piere de Lattre et de trait et san aucuns autre mesus receu LX sous',91);
INSERT INTO "amendes" VALUES (92,6242,60,'défaut_entretien','non','en qoy par le jugement avoit esté condempnez pour faultre de reparacion de chemin trouvée contre son heritage quil tenoit a cause de madamde de Limieux sur le chemin qui maine du Mesnil a Wanvring receu LX sous',92);
INSERT INTO "amendes" VALUES (93,6243,60,'violence_physique','non','avoit batu et manié es mettes dudit bailliage Gillet Robiquet receu LX sous',93);
INSERT INTO "amendes" VALUES (94,6243,60,'violence_physique','non','pour et en nom de Amourriet son nepveu qui estoit rennoméz d avoit batu et manié es mettes dudit bailliagge Hanequin prévost en enfraingan receu LX sous',94);
INSERT INTO "amendes" VALUES (95,6243,60,'violence_physique','non','en nom de Pierot le Mire qui est profere plusieurs langages injurieux contre Catron fille Jehan le Bannier et se avoit avec ce batu sans sang collé Bannier sœur de la dicte Catron receu LX sous',95);
INSERT INTO "amendes" VALUES (96,6243,60,'brigandage','non','demourant a Torcoing pour cause qu'' il avoit entrepris sur l éritage dudit Willement de la Royeur et Quachie le varlet dudit Willement hors de son heritage et oultre le gré dicellui receu LX sous',96);
INSERT INTO "amendes" VALUES (97,6243,26,'conflit_juridiction','non','pour et en l'' acquit de Jehan Carpentier dit du Thuluch pour ce qu'' il comme sergent de monseigneur le chastellain de Lille avoit pris et arresé les bestes de Jehan d'' Antreulles sous la juridiction du seigneur d'' Anelin ou il n avoit qu il veoir ne que congnoissance receu XXVI sous',97);
INSERT INTO "amendes" VALUES (98,6243,60,'évasion','non','pour cause qu'' il japiera il s estoit departis induement hors des fers en de la prison  du seigneur de Bomanches sans le gré et congié d icellui receu LX sous',98);
INSERT INTO "amendes" VALUES (99,6243,26,'vol','non','qu'' elle avoit fait emporté certaine disme qui appartenoit a Jehan Brediere censier de Sanghien oultre le gré ou anmans sans lesteu dicelluy receu XXVI sous',99);
INSERT INTO "amendes" VALUES (100,6243,60,'violence_physique','non','pour et en lacquit de Hanequin et Elinet Baulin feres qui avecq autres estoient souppechonnez davoit batu et manié en paroice Roncq ung nommé Hanequin d Houpplines receu LX sous',100);
INSERT INTO "amendes" VALUES (101,6243,60,'vol','non','elle estoit renommée davoir emporté aucuns bien hors del hostel de Jehan Lambert ou elle demouroit lors sans le gré ou consentement dudit Jehan receu LX sous',101);
COMMIT;
