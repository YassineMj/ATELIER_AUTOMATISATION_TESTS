"""
tests.py — Suite de 6 tests fonctionnels pour l'API Agify.

Chaque fonction retourne un dictionnaire normalisé :
    {"name": str, "status": "PASS"|"FAIL", "latency_ms": float|None, "details": str}

API cible : https://api.agify.io/
L'API Agify prédit l'âge d'une personne à partir de son prénom.
Réponse type : {"count": 234567, "name": "michael", "age": 70}
"""

from tester.client import APIClient

# ── URL de base de l'API publique Agify ──
BASE_URL = "https://api.agify.io"


def _result(name: str, passed: bool, latency_ms, details: str = "") -> dict:
    """Petit helper pour formater uniformément le résultat de chaque test."""
    return {
        "name": name,
        "status": "PASS" if passed else "FAIL",
        "latency_ms": latency_ms,
        "details": details,
    }


# ======================================================================
# TEST 1 — HTTP 200 sur un prénom connu
# ======================================================================
def test_status_200_known_name() -> dict:
    """
    Vérifie que l'endpoint `/?name=michael` renvoie un code HTTP 200.
    'michael' est un prénom très courant, l'API doit répondre sans erreur.
    """
    name = "test_status_200_known_name"
    with APIClient(BASE_URL) as client:
        resp = client.get("/", params={"name": "michael"})

    # Assertion : le code HTTP doit être exactement 200
    passed = resp["status_code"] == 200
    details = (
        "Code 200 reçu comme attendu pour name=michael."
        if passed
        else f"Code inattendu : {resp['status_code']} — {resp.get('error')}"
    )
    return _result(name, passed, resp["latency_ms"], details)


# ======================================================================
# TEST 2 — Content-Type JSON
# ======================================================================
def test_content_type_json() -> dict:
    """
    Vérifie que la réponse de l'API contient bien un header
    Content-Type avec 'application/json'.
    """
    name = "test_content_type_json"
    with APIClient(BASE_URL) as client:
        resp = client.get("/", params={"name": "sarah"})

    # Assertion : le Content-Type doit contenir "application/json"
    content_type = (resp.get("headers") or {}).get("Content-Type", "")
    passed = "application/json" in content_type
    details = (
        f"Content-Type correct : {content_type}"
        if passed
        else f"Content-Type inattendu : '{content_type}'"
    )
    return _result(name, passed, resp["latency_ms"], details)


# ======================================================================
# TEST 3 — Présence des champs obligatoires (count, name, age)
# ======================================================================
def test_required_fields() -> dict:
    """
    Interroge l'API avec un prénom valide et vérifie que les champs
    'count', 'name' et 'age' sont bien présents dans la réponse JSON.
    """
    name = "test_required_fields"
    required_fields = {"count", "name", "age"}

    with APIClient(BASE_URL) as client:
        resp = client.get("/", params={"name": "jean"})

    if resp["status_code"] != 200 or resp["json"] is None:
        return _result(name, False, resp["latency_ms"],
                       f"Impossible d'interroger l'API (status={resp['status_code']})")

    # Assertion : chaque champ obligatoire doit être une clé du dict de réponse
    missing = required_fields - resp["json"].keys()
    passed = len(missing) == 0
    details = (
        f"Tous les champs obligatoires présents : {required_fields}"
        if passed
        else f"Champs manquants : {missing}"
    )
    return _result(name, passed, resp["latency_ms"], details)


# ======================================================================
# TEST 4 — Vérification des types de données
# ======================================================================
def test_data_types() -> dict:
    """
    Vérifie que 'count' est un int, 'name' est un str,
    et 'age' est un int (ou None pour les prénoms très rares).
    """
    name = "test_data_types"

    with APIClient(BASE_URL) as client:
        resp = client.get("/", params={"name": "alice"})

    if resp["status_code"] != 200 or resp["json"] is None:
        return _result(name, False, resp["latency_ms"],
                       f"Impossible d'interroger l'API (status={resp['status_code']})")

    data = resp["json"]

    # Assertions typées
    count_ok = isinstance(data.get("count"), int)           # 'count' doit être un entier
    name_ok = isinstance(data.get("name"), str)              # 'name' doit être une chaîne
    age_ok = isinstance(data.get("age"), (int, type(None)))  # 'age' : int ou None

    passed = count_ok and name_ok and age_ok
    details_parts = []
    if not count_ok:
        details_parts.append(f"'count' n'est pas int (type={type(data.get('count')).__name__})")
    if not name_ok:
        details_parts.append(f"'name' n'est pas str (type={type(data.get('name')).__name__})")
    if not age_ok:
        details_parts.append(f"'age' n'est pas int/None (type={type(data.get('age')).__name__})")
    details = "Types corrects (count=int, name=str, age=int|None)." if passed else " | ".join(details_parts)

    return _result(name, passed, resp["latency_ms"], details)


# ======================================================================
# TEST 5 — Robustesse : paramètre manquant → erreur 422
# ======================================================================
def test_missing_name_returns_error() -> dict:
    """
    Appelle l'API sans fournir le paramètre obligatoire 'name'.
    L'API Agify doit répondre avec un code HTTP 422 (Unprocessable Entity)
    pour signaler l'absence du paramètre requis.
    """
    name = "test_missing_name_returns_error"

    with APIClient(BASE_URL) as client:
        # Appel volontairement sans paramètre 'name'
        resp = client.get("/")

    # Assertion : on s'attend à un code 422 (Missing required parameter)
    passed = resp["status_code"] == 422
    details = (
        "Code 422 reçu comme attendu (paramètre 'name' manquant)."
        if passed
        else f"Code inattendu : {resp['status_code']} (attendu : 422)"
    )
    return _result(name, passed, resp["latency_ms"], details)


# ======================================================================
# TEST 6 — Localisation par pays (country_id)
# ======================================================================
def test_country_id_parameter() -> dict:
    """
    Vérifie que l'endpoint accepte le paramètre optionnel 'country_id'
    (ex: ?name=michael&country_id=US) et retourne un code 200
    avec le champ 'country_id' présent dans la réponse.
    """
    name = "test_country_id_parameter"

    with APIClient(BASE_URL) as client:
        resp = client.get("/", params={"name": "michael", "country_id": "US"})

    if resp["status_code"] != 200 or resp["json"] is None:
        return _result(name, False, resp["latency_ms"],
                       f"Endpoint indisponible (status={resp['status_code']})")

    data = resp["json"]

    # Assertion : le champ 'country_id' doit être présent et valoir 'US'
    has_country = data.get("country_id") == "US"
    passed = has_country
    details = (
        f"Paramètre country_id=US accepté — réponse : age={data.get('age')}, count={data.get('count')}."
        if passed
        else f"Champ 'country_id' absent ou incorrect : {data.get('country_id')}"
    )
    return _result(name, passed, resp["latency_ms"], details)


# ======================================================================
# Point d'entrée — exécution de toute la suite de tests
# ======================================================================
if __name__ == "__main__":
    tests = [
        test_status_200_known_name,
        test_content_type_json,
        test_required_fields,
        test_data_types,
        test_missing_name_returns_error,
        test_country_id_parameter,
    ]

    print("=" * 65)
    print("  SUITE DE TESTS — API Agify (Testing as Code)")
    print("=" * 65)

    total, passed_count = len(tests), 0
    for test_fn in tests:
        result = test_fn()
        status_icon = "✅" if result["status"] == "PASS" else "❌"
        print(f"\n{status_icon}  {result['name']}")
        print(f"    Status  : {result['status']}")
        print(f"    Latence : {result['latency_ms']} ms")
        print(f"    Détails : {result['details']}")
        if result["status"] == "PASS":
            passed_count += 1

    print("\n" + "=" * 65)
    print(f"  RÉSULTAT : {passed_count}/{total} tests réussis")
    print("=" * 65)
