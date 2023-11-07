from eNB import eNB

# Mix Environment
en1_1 = eNB(40000, "lte")
en1_2 = eNB(15000, "lte")
en1_3 = eNB(5000, "nr")
en1_4 = eNB(35000, "nr")
en1_5 = eNB(25000, "nr")
en1_6 = eNB(20000, "nr")
en1_7 = eNB(45000, "nr")
en1_8 = eNB(10000, "nr")
en1_9 = eNB(12000, "nr")
en1_10 = eNB(30000, "nr")
eNBs_mix1 = ("NR-LTE-Mix1", [en1_1, en1_2, en1_3, en1_4, en1_5, en1_6, en1_7, en1_8, en1_9, en1_10])

# LTE Environment
en2_1 = eNB(10000, "lte")
en2_2 = eNB(40000, "lte")
en2_3 = eNB(25000, "lte")
eNBs_lte = ("LTE", [en2_1, en2_2, en2_3])

# NR Environment
en3_1 = eNB(5000, "nr")
en3_2 = eNB(15000, "nr")
en3_3 = eNB(25000, "nr")
en3_4 = eNB(35000, "nr")
en3_5 = eNB(45000, "nr")
eNBs_nr = ("NR", [en3_1, en3_2, en3_3, en3_4])
