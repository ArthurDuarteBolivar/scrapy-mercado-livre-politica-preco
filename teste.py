new_name = "Fonte Automotiva Jfa Storm Lite 70a Bivolt Carregador".lower()

if "bob" not in new_name and "lite" not in new_name and "light" not in new_name  and "controle" not in new_name and 'jfa' in new_name and "usina" not in new_name:
    if "70a" in new_name or "70" in new_name or "70 amperes" in new_name or "70amperes" in new_name or "70 a" in new_name:
        print(new_name)
        
if "bob" not in new_name and  ("lite" in new_name or "light" in new_name) and "controle" not in new_name and 'jfa' in new_name and "usina" not in new_name:
    if "70a" in new_name or "70" in new_name or "70 amperes" in new_name or "70amperes" in new_name or "70 a" in new_name:
        print(new_name)