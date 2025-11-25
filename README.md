# 👻 GhostBusters - Advanced 2D Platformer Game

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen.svg)

Un jeu de plateforme 2D avancé développé en Python avec Pygame, featuring un système de compétences progressives, des mécaniques de mouvement sophistiquées, et des combats dynamiques contre des fantômes.

![GhostBusters Game](app.png)

## 🎮 Aperçu du Jeu

GhostBusters est un jeu de plateforme où vous incarnez un chasseur de fantômes équipé d'armes et de capacités spéciales. Traversez 3 niveaux challengeants, débloquez de nouvelles compétences, et affrontez des ennemis avec une IA avancée.

### ✨ Fonctionnalités Principales

#### 🏃‍♂️ **Système de Mouvement Avancé**
- **Sprint** : Course rapide (SHIFT)
- **Double Saut** : Saut supplémentaire en l'air
- **Wall-Grab** : Accrochage aux murs avec système de stamina
- **Wall-Climb** : Montée et descente le long des murs
- **Wall-Jump** : Saut puissant depuis l'accrochage

#### ⚔️ **Système de Combat**
- **Pistolet** : Arme de base avec munitions illimitées
- **Shotgun** : Tir en éventail avec munitions limitées
- **Grenades** : Explosifs à zone d'effet
- **Système de dégâts** : Effets visuels et invulnérabilité temporaire

#### 🌟 **Compétences Progressives**
- **Niveau 1 → 2** : **Charge Shot** - Tir chargé avec 3 niveaux de puissance
- **Niveau 2 → 3** : **Bouclier** + **Mode Rafale** - Protection et tir automatique

#### 👻 **Ennemis Intelligents**
- **Fantômes au Sol** : Patrouille et poursuite du joueur
- **Fantômes Volants** : IA aérienne avec limites d'écran
- **Système de Vie** : Ennemis résistants avec feedback visuel

#### 💥 **Effets Visuels**
- **Particules** : Explosions, trails, charge d'énergie
- **Screen Shake** : Secousse d'écran lors des impacts
- **Damage Effects** : Clignotement et effets colorés
- **UI Dynamique** : Barres de vie, stamina, compétences

## 🎯 Contrôles

### Mouvements de Base
- **←/→** : Déplacement gauche/droite
- **↑** : Saut (double saut disponible)
- **SHIFT** : Sprint (vitesse x2)

### Combat
- **ESPACE** : Tir / Charge Shot (après déblocage)
- **G** : Lancer une grenade
- **TAB** : Changer d'arme (Pistolet ↔ Shotgun)

### Compétences Avancées
- **C** : S'accrocher au mur (Wall-Grab)
- **W/S** : Monter/Descendre sur le mur (en mode Wall-Grab)
- **V** : Activer le bouclier (après déblocage niveau 2)
- **X** : Activer le mode rafale (après déblocage niveau 2)

## 🎪 Progression du Jeu

### Niveau 1
- Introduction aux mécaniques de base
- Apprentissage du mouvement et du combat
- **Récompense** : Déblocage du **Charge Shot**

### Niveau 2
- Défis de plateforme plus complexes
- Utilisation du Charge Shot
- **Récompense** : Déblocage du **Bouclier** et **Mode Rafale**

### Niveau 3
- Boss fight et défis ultimes
- Utilisation de toutes les compétences
- **Victoire** : Fin du jeu

## 🛠️ Installation et Lancement

### Prérequis
- Python 3.10 ou supérieur
- Pygame 2.6.1 ou supérieur

### Installation
```bash
# Cloner le repository
git clone https://github.com/Marwen225/game-ghost.git
cd game-ghost

# Installer les dépendances
pip install pygame

# Lancer le jeu
python main.py
# ou
python3 main.py
```

## 📁 Structure du Projet

```
GhostBusters/
├── main.py              # Point d'entrée principal
├── player.py             # Classe joueur avec compétences
├── enemies.py            # IA des ennemis
├── projectiles.py        # Système de projectiles
├── particles.py          # Effets visuels
├── world.py              # Gestion des niveaux
├── button.py             # Interface utilisateur
├── texts.py              # Système de texte
├── level_editor.py       # Éditeur de niveaux
├── Assets/               # Sprites et images
│   ├── Player/           # Animations du joueur
│   ├── Ghost/            # Animations des ennemis
│   └── Tiles/            # Tuiles de niveau
├── Sounds/               # Effets sonores
├── Fonts/                # Polices personnalisées
├── Levels/               # Données des niveaux
└── Data/                 # Fichiers de configuration
```

## 🔧 Architecture Technique

### Classes Principales
- **Player** : Gestion du joueur, compétences, animations
- **Ghost/FlyingGhost** : IA des ennemis
- **Bullet/Grenade** : Système de projectiles
- **Particle Effects** : Effets visuels
- **World** : Gestion des niveaux et collisions

### Systèmes Avancés
- **Skill System** : Déblocage progressif de compétences
- **State Management** : Gestion des états du jeu
- **Collision Detection** : Système de collision pixel-perfect
- **Audio System** : Effets sonores et musique
- **Save System** : Persistance des compétences entre niveaux

## 🎨 Assets et Ressources

- **Sprites** : Animations frame par frame pour joueur et ennemis
- **Backgrounds** : Parallax scrolling multi-couches
- **Sound Effects** : Audio dynamique pour actions et events
- **Fonts** : Polices thématiques pour l'interface

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 Changelog

### Version 1.0.0 (Actuelle)
- ✅ Système de mouvement complet (sprint, double saut, wall-grab)
- ✅ Compétences progressives (Charge Shot, Bouclier, Mode Rafale)
- ✅ IA des ennemis (fantômes au sol et volants)
- ✅ Effets visuels avancés (particules, screen shake)
- ✅ 3 niveaux de difficulté progressive
- ✅ Système de combat multi-armes
- ✅ Interface utilisateur dynamique

## 🐛 Bugs Connus
Aucun bug majeur connu. Rapportez les problèmes via les Issues GitHub.

## 📜 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

**Marwen225** - [GitHub Profile](https://github.com/Marwen225)

---

⭐ **N'hésitez pas à star le repo si vous avez aimé le jeu !** ⭐