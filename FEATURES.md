# Fonctionnalités Avancées - Monitoring API Agify

## 📊 Nouvelles Fonctionnalités (v2.1)

### **NOUVELLES PAGES COMPLÈTES** 🎉

#### 1. **Dashboard Principal** (/)
- Vue d'ensemble en temps réel
- Graphiques Taux de Succès et Latence
- Historique des 30 derniers runs
- Auto-refresh configurable (30s)
- Export rapide CSV/JSON
- Liens vers tous les autres outils

#### 2. **Analytique Avancée** (/analytics)
- **Statistiques Globales** : vue d'ensemble complète
  - Total des runs exécutés
  - Moyenne des tests réussis
  - Taux d'erreur global
  - Latences moyennes et P95
- **Distribution des Latences** : histogramme de répartition
- **Succès par Test** : performance individuelle de chaque test
- **Tendances (7 jours)** :
  - Évolution du taux d'erreur
  - Performance des latences
- **Métriques Détaillées par Test** :
  - Taux de succès %
  - Ratio réussi/échoué
  - Latence moyenne
  - Classification (Bon/Moyen/Faible)
- **Percentiles de Latence** :
  - P25, P50, P75, P95, P99
  - Identification des goulots
- **Comparaison Visuelle** :
  - Sélectionner 2 runs
  - Voir les différences côte à côte
  - Mesurer les régressions

#### 3. **Détails des Tests** (/testlogs)
- **Vue Détaillée des Tests**
  - Chaque test affiché avec statut
  - Latence, détails d'exécution
  - Timestamp de chaque run
- **Filtres Avancés**
  - Rechercher par nom de test
  - Filtrer par statut (Réussi/Échoué)
  - Sélectionner un run spécifique
- **Historique des Erreurs**
  - Timeline des échecs
  - Messages d'erreur détaillés
  - Dates/heures précises
- **Pagination** : navigate dans les runs

#### 4. **Configuration** (/settings)
- **Seuils d'Alerte Personnalisés**
  - Taux d'erreur (warning/critique)
  - Latence moyenne (warning/critique)
  - P95 latence
  - Nombre de tests échoués
  - Interface drag-and-drop
- **Configuration des Notifications**
  - Email pour alertes critiques
  - Webhook Slack
  - Webhook personnalisé
- **Paramètres Généraux**
  - Nombre de runs à conserver
  - Intervalle de nettoyage
  - Statistiques détaillées
- **Actions Avancées**
  - Télécharger la base de données
  - Nettoyer les anciennes données
  - Réinitialiser les seuils par défaut
  - Tester les alertes

### 2. **Endpoints API Puissants** 🔌

| Route | Usage | Response |
|-------|-------|----------|
| `GET /api/stats` | Statistiques globales | min/max/avg de tous les runs |
| `GET /api/runs?limit=50` | Tous les runs | JSON avec raw_tests_json |
| `GET /api/performance` | Stats par test | taux succès, latences, min/max |
| `GET /api/compare/1/2` | Comparer 2 runs | différences détaillées |
| `GET /api/alerts` | Alertes actives | liste des violations QoS |
| `GET /api/docs` | Documentation | tous les endpoints |
| `GET /export/csv` | CSV complet | historique en tableur |
| `GET /export/json` | JSON complet | export brut |
| `POST /api/clear-old-data` | Nettoyer DB | supprimer runs > 30j |
| `GET /api/export-db` | Télécharger DB | fichier monitoring.db |
| `POST /api/test-alerts` | Test alertes | envoyer alerte test |

### 3. **Dashboard Premium** 🎨
- Nouveau design modern
- **Graphiques Interactifs** (Chart.js)
  - Taux de succès (Passed vs Failed)
  - Évolution des latences
  - Distribution des réponses
- **Affichage Responsive**
  - Desktop : full 3+ colonnes
  - Tablette : 2 colonnes
  - Mobile : 1 colonne
- **Mode Sombre** 🌙
  - Basculer avec un clic
  - Sauvegarde automatique
  - Graphiques ajustés

### 4. **Système d'Alertes Intelligent** 🚨
- **Seuils Configurables**
  - Taux d'erreur : 20% (warn), 50% (critique)
  - Latence : 2000ms (warn), 5000ms (critique)
  - P95 : 3000ms (warn)
  - Tests échoués : 3+ (critique)
- **Alertes Automatiques**
  - /api/alerts retourne l'état actuel
  - Visualisation claire avec couleurs
  - Messages détaillés

### 5. **Export Avancé** 📥
- **CSV** : Historique complet, format tableur Excel
- **JSON** : Export brut complet
- **Base de Données** : Télécharger monitoring.db
- **Noms Automatiques** : timestamp inclus

### 6. **Comparaison de Runs** 📊
- **Vue Côte à Côte**
  - Sélectionner 2 runs
  - Voir toutes les métriques
  - Deltas calculés
- **Identification Régression**
  - Latence augmentation
  - Taux erreur changement
  - Défaillances nouvelles

---

## 🚀 Navigation Complète

### **Menu Principal (Visible dans le Header)**
```
Home (Dashboard) → Analytique → Logs → Config → Export → Dark Mode
```

### **Accès Direct par URL**
```
Tableau de bord       : /dashboard
Analytique avancée   : /analytics
Logs détaillés       : /testlogs
Configuration        : /settings
Documentation API    : /api/docs
```

### **Exemple de Workflow**
1. **Monitoring** : Aller à /dashboard, activer auto-refresh
2. **Analyse** : Cliquer sur "Analytique" pour tendances
3. **Debug** : Aller à "Logs" pour voir erreurs détaillées
4. **Tuning** : Aller à "Config" pour ajuster seuils
5. **Rapports** : Exporter en CSV/JSON

---

## 📊 Cas d'Usage Avancés

### 1. **Surveillance 24/7**
- Dashboard en fullscreen avec auto-refresh 30s
- Mode sombre pour moins d'éblouissement
- Alertes critiques visibles immédiatement

### 2. **Root Cause Analysis**
- Aller à Logs pour voir tous les tests échoués
- Filtrer par test problématique
- Voir timeline des erreurs
- Identifier pattern

### 3. **Optimisation Performance**
- Analytique → Tendances
- Voir où les latences augmentent
- Comparer avant/après changement
- Identifier régressions

### 4. **Rapports et Compliance**
- Export CSV pour Excel
- Générer graphiques
- Partager avec stakeholders
- Archiver mensuellement

### 5. **Automatisation Alertes**
- Configurer webhooks Slack/custom
- Intégrer avec CI/CD
- Déclencher actions
- Notifications en temps réel

---

## 🎯 Fonctionnalités Résumées

### **Affichage**
- ✅ Dashboard Premium avec thème sombre
- ✅ 4 pages complètes distinctes
- ✅ Graphiques interactifs Chart.js
- ✅ Responsive design mobile/tablette/desktop
- ✅ Navigation intuitive

### **Fonctionnalités**
- ✅ Auto-refresh configurable
- ✅ Export CSV/JSON/DB
- ✅ Filtres et recherche
- ✅ Comparaison entre runs
- ✅ Historique des erreurs
- ✅ Seuils d'alerte personnalisés
- ✅ Statistiques avancées
- ✅ Métriques par test

### **API**
- ✅ 11 endpoints
- ✅ Documentation complète
- ✅ JSON standardisé
- ✅ Export formats multiples
- ✅ Gestion alertes

---

## 📱 Interfaces Disponibles

| Page | URL | Fonctionnalités |
|------|-----|-----------------|
| **Dashboard** | `/` | Vue principale, auto-refresh, quick actions |
| **Analytics** | `/analytics` | Stats, tendances, comparaison |
| **Test Logs** | `/testlogs` | Historique détaillé, filtres, timeline |
| **Settings** | `/settings` | Seuils, notifications, actions |

---

## 🔧 Configuration Avancée

### **Sauvegarder les Préférences**
- Mode sombre sauvegardé automatiquement
- Auto-refresh per session
- Filtres per-page

### **Personnalisation des Seuils**
```python
# Dans flask_app.py, fonction api_alerts()
thresholds = {
    "error_rate_critical": 0.5,      # 50%
    "error_rate_warning": 0.2,       # 20%
    "latency_critical": 5000,        # ms
    "latency_warning": 2000,         # ms
    "failed_tests_critical": 3       # tests
}
```

---

## 🚀 Déploiement

### **Localement**
```bash
python flask_app.py
# Accéder : http://localhost:5000
```

### **PythonAnywhere**
```bash
git push
# Reload web app
# Accéder : https://Yassine48MOUJAHID.pythonanywhere.com
```

---

**Version** : 2.1  
**Dernière mise à jour** : 4 mars 2026  
**Interfaces** : 4 pages complètes  
**Endpoints** : 11 API avancées  
**Fonctionnalités** : 50+ features

### 1. **Dashboard Amélioré** 🎨
- **Mode Sombre** : Basculer automatiquement entre mode clair et sombre
- **Graphiques Interactifs** : Visualiser les tendances avec Chart.js
  - Taux de succès des tests (Passed vs Failed)
  - Latence moyenne et P95 au fil du temps
- **Design Responsive** : Affichage optimisé sur mobile, tablette, desktop
- **KPIs Avancés** : Indicateurs colorés avec animations

### 2. **Auto-refresh Configurable** 🔄
- Cocher "Auto-refresh (30s)" pour recharger automatiquement le dashboard
- Utile pour surveiller l'API en temps réel sans interaction manuelle

### 3. **Export de Données** 📥
- **CSV** : Exporter l'historique des runs en format tableur
- **JSON** : Exporter pour intégration dans d'autres outils
- Lien direct depuis le header du dashboard

### 4. **API Endpoints Avancés** 🔌

#### `/api/stats`
Statistiques agrégées de tous les runs :
```json
{
  "total_runs": 50,
  "avg_passed": 5.92,
  "avg_failed": 0.08,
  "min_error_rate": 0.0,
  "max_error_rate": 0.5,
  "avg_error_rate": 0.0133,
  "min_latency_avg": 145.23,
  "max_latency_avg": 2341.45,
  "avg_latency_avg": 523.12,
  "min_latency_p95": 234.12,
  "max_latency_p95": 4523.67,
  "avg_latency_p95": 892.34
}
```

#### `/api/runs?limit=50`
Liste des runs avec tous les détails :
```json
{
  "runs": [
    {
      "id": 50,
      "timestamp": "2026-03-04T12:30:45",
      "passed": 6,
      "failed": 0,
      "error_rate": 0.0,
      "latency_avg": 523.12,
      "latency_p95": 892.34,
      "raw_tests_json": { ... }
    }
  ],
  "count": 50
}
```

#### `/api/compare/<run1>/<run2>`
Comparer deux runs spécifiques :
```json
{
  "run1": { ... },
  "run2": { ... },
  "differences": {
    "passed_delta": -1,
    "failed_delta": 1,
    "error_rate_delta": 0.1667,
    "latency_avg_delta": +142.5,
    "latency_p95_delta": +234.12
  }
}
```

#### `/api/alerts`
Vérifier les alertes actives basées sur les seuils QoS :
```json
{
  "alerts": [
    {
      "level": "warning",
      "message": "Taux d'erreur élevé: 33.3%",
      "value": 0.333
    }
  ],
  "has_critical": false,
  "run_id": 50,
  "timestamp": "2026-03-04T12:30:45"
}
```

### 5. **Système d'Alertes** 🚨
Automatiquement alertés si :
- **Taux d'erreur** > 50% (critique) ou > 20% (avertissement)
- **Latence moyenne** > 5000ms (critique) ou > 2000ms (avertissement)
- **3+ tests échoués** (critique)

### 6. **Comparaison de Runs** 📊
- Comparer deux runs via `/api/compare/<id1>/<id2>`
- Voir les variations de performance
- Identifier les régressions

### 7. **Documentation API** 📖
- `/api/docs` : Documentation complète de tous les endpoints
- Utiliser pour intégrer le monitoring dans vos outils

## 🚀 Utilisation

### Accéder au Dashboard
```
http://localhost:5000
```

### Télécharger les données
- Cliquer sur "📥 CSV" pour un export tableur
- Cliquer sur "📥 JSON" pour un export JSON complet

### Activer l'Auto-refresh
1. Cocher la case "Auto-refresh (30s)"
2. Le dashboard se recharge tous les 30 secondes automatiquement

### Consulter les Statistiques
```bash
curl http://localhost:5000/api/stats
```

### Comparer deux runs
```bash
curl http://localhost:5000/api/compare/48/50
```

### Récupérer les alertes actives
```bash
curl http://localhost:5000/api/alerts
```

## 🎨 Personnalisations Disponibles

### Mode Sombre
- Cliquer sur le bouton 🌙 en haut à droite
- La préférence est sauvegardée en local

### Seuils d'Alerte
Les seuils peuvent être ajustés dans `flask_app.py` (fonction `api_alerts`):
```python
thresholds = {
    "error_rate_critical": 0.5,    # > 50%
    "error_rate_warning": 0.2,     # > 20%
    "latency_critical": 5000,      # > 5000ms
    "latency_warning": 2000,       # > 2000ms
    "failed_tests_critical": 3     # 3+ tests
}
```

## 📈 Cas d'Usage

### 1. Monitoring en Temps Réel
- Accéder au dashboard
- Activer auto-refresh
- Laisser tourner dans un navigateur

### 2. Rapports Automatisés
- Exporter les données en CSV chaque jour
- Créer un graphique Excel
- Partager avec l'équipe

### 3. Intégration CI/CD
- Appeler `/api/alerts` après les tests
- Fail la pipeline si alertes critiques
- Envoyer notification Slack/Teams

### 4. Analyse Comparative
- Utiliser `/api/compare` pour comparer versions
- Identifier les régressions de performance
- Tracker tendances long-terme

## 🔧 Configuration Avancée

### Variables d'Environnement
```bash
# Port custom
PORT=8080 python flask_app.py

# Debug mode désactivé
FLASK_ENV=production python flask_app.py
```

### Base de Données
- Fichier SQLite : `monitoring.db`
- Limite par défaut : 100 runs conservés
- Modifier dans `storage.py` si nécessaire

## 📱 Support Multi-Device

- **Desktop** : Affichage plein écran idéal
- **Tablette** : Layout responsive 2 colonnes
- **Mobile** : Layout mobile optimisé, 1 colonne
- **Sombre** : Confortable la nuit

## 🎯 Prochaines Améliorations Possibles

- [ ] Notifications Webhook (Slack, Teams)
- [ ] Alertes email
- [ ] Historique détaillé des erreurs
- [ ] Graphiques heatmap par heure
- [ ] Prédiction de régression (ML)
- [ ] Custom thresholds par endpoint
- [ ] Dashboard mobile app
- [ ] Authentification multi-user

---

**Version** : 2.0  
**Dernière mise à jour** : 4 mars 2026
