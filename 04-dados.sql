# patogeno
INSERT INTO patogeno (id, nome, tipo) VALUES 
(1, 'Mycobacterium tuberculosis', 'Bactéria'),
(2, 'Influenza virus', 'Vírus'),
(3, 'Plasmodium spp.', 'Parasita'),
(4, 'Dengue virus', 'Vírus'),
(5, 'Hepatitis B virus', 'Vírus'),
(6, 'Treponema pallidum', 'Bactéria'),
(7, 'Candida albicans', 'Fungo'),
(8, 'Varicella-zoster virus', 'Vírus'),
(9, 'Leptospira spp.', 'Bactéria'),
(10, 'Toxoplasma gondii', 'Parasita'),
(11, 'Neisseria meningitidis', 'Bactéria'),
(12, 'Yellow fever virus', 'Vírus'),
(13, 'Zika virus', 'Vírus'),
(14, 'Chikungunya virus', 'Vírus'),
(15, 'Rubella virus', 'Vírus'),
(16, 'Measles virus', 'Vírus'),
(17, 'Clostridium tetani', 'Bactéria'),
(18, 'Mycobacterium leprae', 'Bactéria'),
(19, 'Vibrio cholerae', 'Bactéria'),
(20, 'Salmonella typhi', 'Bactéria'),
(21, 'Poliovirus', 'Vírus'),
(22, 'Rabies virus', 'Vírus'),
(23, 'Schistosoma spp.', 'Parasita'),
(24, 'Giardia lamblia', 'Parasita'),
(25, 'Entamoeba histolytica', 'Parasita'),
(26, 'Trichomonas vaginalis', 'Parasita'),
(27, 'Trypanosoma cruzi', 'Parasita'),
(28, 'Leishmania spp.', 'Parasita'),
(29, 'Epstein-Barr virus', 'Vírus'),
(30, 'Mumps virus', 'Vírus'),
(31, 'Hepatitis A virus', 'Vírus'),
(32, 'Hepatitis C virus', 'Vírus'),
(33, 'Herpes simplex virus', 'Vírus'),
(34, 'Variola virus', 'Vírus');

# doenca
INSERT INTO doença (id, nome_tecnico, CID, id_patogeno) VALUES 
(1, 'Tuberculose', 'A15-A19', 1),
(2, 'Gripe', 'J10-J11', 2),
(3, 'Malária', 'B50-B54', 3),
(4, 'Dengue', 'A90', 4),
(5, 'Hepatite B', 'B16', 5),
(6, 'Sífilis', 'A50-A53', 6),
(7, 'Candidíase', 'B37', 7),
(8, 'Varicela', 'B01', 8),
(9, 'Leptospirose', 'A27', 9),
(10, 'Toxoplasmose', 'B58', 10),
(11, 'Meningite', 'G00-G03', 11),
(12, 'Febre Amarela', 'A95', 12),
(13, 'Zika', 'A92.5', 13),
(14, 'Chikungunya', 'A92.0', 14),
(15, 'Rubéola', 'B06', 15),
(16, 'Sarampo', 'B05', 16),
(17, 'Tétano', 'A33-A35', 17),
(18, 'Hanseníase', 'A30', 18),
(19, 'Cólera', 'A00', 19),
(20, 'Tifoide', 'A01.0', 20),
(21, 'Poliomielite', 'A80', 21),
(22, 'Raiva', 'A82', 22),
(23, 'Esquistossomose', 'B65', 23),
(24, 'Giardíase', 'A07.1', 24),
(25, 'Amebíase', 'A06', 25),
(26, 'Tricomoníase', 'A59', 26),
(27, 'Doença de Chagas', 'B57', 27),
(28, 'Leishmaniose', 'B55', 28),
(29, 'Tétano Neonatal', 'A33', 17),
(30, 'Hepatite A', 'B15', 31),
(31, 'Hepatite C', 'B17.1', 32),
(32, 'Herpes Simples', 'B00', 33),
(33, 'Mononucleose', 'B27', 29),
(34, 'Caxumba', 'B26', 30),
(35, 'Varíola', 'B03', 34);

# nomes populares
INSERT INTO nomes_populares (doença_id, nome) VALUES 
(7, 'Sapinho'),
(8, 'Catapora'),
(18, 'Lepra'),
(23, 'Barriga dágua'),
(33, 'Doença do Beijo'),
(34, 'Papeira');

# sintomas
INSERT INTO sintomas (id, nome) VALUES 
(1, 'Tosse'),
(2, 'Febre'),
(3, 'Perda de peso'),
(4, 'Dor de cabeça'),
(5, 'Fadiga'),
(6, 'Calafrios'),
(7, 'Dor muscular'),
(8, 'Erupção cutânea'),
(9, 'Icterícia'),
(10, 'Dor abdominal'),
(11, 'Úlceras'),
(12, 'Coceira'),
(13, 'Corrimento'),
(14, 'Dor ao urinar'),
(15, 'Perda de sensibilidade'),
(16, 'Náusea'),
(17, 'Desidratação'),
(18, 'Vômito'),
(19, 'Paralisia'),
(20, 'Espasmos musculares'),
(21, 'Rigidez'),
(22, 'Dor de garganta'),
(23, 'Dor articular'),
(24, 'Ínguas'),
(25, 'Manchas na pele'),
(26, 'Fraqueza muscular'),
(27, 'Inchaço no local da picada'),
(28, 'Diarreia'),
(29, 'Inchaço nas glândulas'),
(30, 'Feridas na pele'),
(31, 'Rigidez de nuca');

# frequencia
INSERT INTO apresenta (doença_id, sintoma_id, frequencia) VALUES 
(1, 1, 'muito comum'),
(1, 2, 'comum'),
(1, 3, 'comum'),

(2, 2, 'muito comum'),
(2, 4, 'comum'),
(2, 5, 'comum'),

(3, 2, 'muito comum'),
(3, 6, 'muito comum'),
(3, 4, 'comum'),

(4, 2, 'muito comum'),
(4, 7, 'comum'),
(4, 8, 'comum'), 

(5, 9, 'comum'),
(5, 5, 'comum'),
(5, 10, 'comum'),

(6, 11, 'comum'),
(6, 8, 'comum'),
(6, 2, 'pouco comum'),

(7, 12, 'muito comum'),
(7, 13, 'comum'),
(7, 14, 'pouco comum'),

(8, 8, 'muito comum'),
(8, 2, 'comum'),
(8, 12, 'comum'),

(9, 2, 'muito comum'),
(9, 7, 'comum'),
(9, 9, 'pouco comum'),

(10, 2, 'pouco comum'),
(10, 7, 'pouco comum'),
(10, 24, 'pouco comum'),

(11, 2, 'muito comum'),
(11, 4, 'muito comum'),
(11, 31, 'comum'),

(12, 2, 'muito comum'),
(12, 9, 'comum'),
(12, 7, 'comum'),

(13, 2, 'comum'),
(13, 8, 'comum'),
(13, 23, 'comum'),

(14, 2, 'muito comum'),
(14, 23, 'muito comum'),
(14, 8, 'comum'),

(15, 8, 'muito comum'),
(15, 2, 'comum'),
(15, 24, 'comum'),

(16, 8, 'muito comum'),
(16, 2, 'muito comum'),
(16, 1, 'comum'),

(17, 20, 'muito comum'),
(17, 21, 'muito comum'),
(17, 8, 'pouco comum'),

(18, 25, 'muito comum'),
(18, 15, 'comum'),
(18, 26, 'pouco comum'),

(19, 28, 'muito comum'),
(19, 18, 'comum'),
(19, 17, 'comum'),

(20, 2, 'muito comum'),
(20, 10, 'muito comum'),
(20, 8, 'pouco comum'),

(21, 19, 'muito comum'),
(21, 2, 'comum'),
(21, 7, 'comum'),

(22, 2, 'muito comum'),
(22, 4, 'comum'),
(22, 20, 'comum'),

(23, 2, 'comum'),
(23, 10, 'comum'),
(23, 28, 'pouco comum'),

(24, 28, 'muito comum'),
(24, 20, 'comum'),
(24, 26, 'comum'),

(25, 28, 'muito comum'),
(25, 10, 'comum'),
(25, 2, 'comum'),

(26, 13, 'muito comum'),
(26, 12, 'comum'),
(26, 14, 'pouco comum'),

(27, 2, 'comum'),
(27, 27, 'comum'),
(27, 10, 'pouco comum'),

(28, 30, 'muito comum'),
(28, 2, 'comum'),
(28, 3, 'comum'),

(29, 20, 'muito comum'),
(29, 21, 'muito comum'),
(29, 2, 'pouco comum'),

(30, 9, 'comum'),
(30, 5, 'comum'),
(30, 10, 'comum'),

(31, 9, 'comum'),
(31, 5, 'comum'),
(31, 10, 'comum'),

(32, 30, 'muito comum'),
(32, 12, 'comum'),
(32, 14, 'pouco comum'),

(33, 2, 'muito comum'),
(33, 22, 'comum'),
(33, 5, 'comum'),

(34, 29, 'muito comum'),
(34, 2, 'comum'),
(34, 4, 'comum'),

(35, 8, 'muito comum'),
(35, 2, 'muito comum'),
(35, 7, 'comum');