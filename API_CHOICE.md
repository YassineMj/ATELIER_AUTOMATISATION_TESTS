# API Choice

- Étudiant : Yassine MOUJAHID
- API choisie : Agify
- URL base : https://api.agify.io
- Documentation officielle / README : https://agify.io/documentation
- Auth : None
- Endpoints testés :
  - GET /?name=michael
  - GET /?name=john
- Hypothèses de contrat (champs attendus, types, codes) :
  - status code 200
  - JSON
  - champs : name (string), age (int ou null), count (int)
- Limites / rate limiting connu :
  - Pas strictement documenté mais usage raisonnable requis
- Risques :
  - Latence variable
  - null possible sur age