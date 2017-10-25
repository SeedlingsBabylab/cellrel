import pyclan as pc



cf = "data/02_15_CMedit.cha"


clan_file = pc.ClanFile(cf)

clan_file.flatten()
clan_file.annotate()
clan_file.assign_pho()



# x = clan_file.line_map[17700:]
annots = clan_file.annotations()
clan_file.delete_pho_comments()
print

clan_file.basic_level("bl_output2.csv")

print

