from params import bot_a_correr
from bots.fbl5n_diario.fbl5n_diario import fbl5n_diario
from bots.fbl5n_cierre.fbl5n_cierre import fbl5n_cierre

if (bot_a_correr == "fbl5n_diario"):
  print(f'Running bot: {bot_a_correr}')
  fbl5n_diario()
elif (bot_a_correr == "fbl5n_cierre"):
  print(f'Running bot: {bot_a_correr}')
  fbl5n_cierre()