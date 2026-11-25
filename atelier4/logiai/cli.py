
import argparse
import json
import sys
from pathlib import Path

from logiai.predict import Predictor


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="logiai-predict")
    parser.add_argument("fichier", help="Fichier JSON d'une livraison")
    args = parser.parse_args(argv)

    chemin = Path(args.fichier)

    if not chemin.exists():
        print(f"Fichier introuvable : {chemin}", file=sys.stderr)
        return 1

    try:
        livraison = json.loads(chemin.read_text(encoding="utf-8-sig"))
        resultat = Predictor().predict(livraison)
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        print(f"Erreur de lecture ou de prÃ©diction : {exc}", file=sys.stderr)
        return 1

    probabilite = resultat["probabilite_retard"] * 100
    statut = "ALERTE" if resultat["alerte"] else "PAS D'ALERTE"

    print(
        f"ProbabilitÃ© de retard : {probabilite:.0f} % "
        f"({statut}) â€” seuil : {resultat['seuil']}"
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
