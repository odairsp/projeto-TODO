atividades = [
    {
        "ativitname": "atividade1", 'username': "odair"
    },
   
    {
        "ativitname": "atividade2", 'username': "odair"
    },
   
    {
        "ativitname": "atividade3", 'username': "odair"
    },
   
    {
        "ativitname": "atividade4", 'username': "joao"
    },
   
    {
        "ativitname": "atividade5", 'username': "joao"
    },
   
    {
        "ativitname": "atividade6", 'username': "joao"
    },
   
    {
        "ativitname": "atividade7", 'username': "odair"
    }
   
]

for atv in atividades:
    atv['username'] = "jose"
    print(atv)
