import json
import os


def criar_exemplo_squad(
    contexto,
    pergunta,
    resposta="",
    resposta_plausivel=""
):

    is_impossible = resposta.strip() == ""

    qa = {
        "id": f"id_{abs(hash(pergunta))}",
        "question": pergunta,
        "is_impossible": is_impossible,
        "answers": [],
        "plausible_answers": []
    }

    if not is_impossible:

        answer_start = contexto.find(resposta)

        if answer_start == -1:
            raise ValueError(
                "A resposta não foi encontrada dentro do contexto."
            )

        qa["answers"].append({
            "text": resposta,
            "answer_start": answer_start
        })

    elif resposta_plausivel:

        answer_start = contexto.find(
            resposta_plausivel
        )

        qa["plausible_answers"].append({
            "text": resposta_plausivel,
            "answer_start": answer_start
        })

    return {
        "context": contexto,
        "qas": [qa]
    }


def adicionar_exemplo(dataset, exemplo):

    contexto_novo = exemplo["context"]

    for item in dataset["data"]:

        if item["context"] == contexto_novo:

            item["qas"].extend(
                exemplo["qas"]
            )

            return

    dataset["data"].append(exemplo)


def normalizar_texto(texto):
    return " ".join(
        texto.strip().lower().split()
    )


def fazer_merge_squad(
    arquivo_principal,
    arquivo_novo,
    arquivo_saida
):

    if not os.path.exists(
        arquivo_principal
    ):
        raise FileNotFoundError(
            f"Arquivo não encontrado: "
            f"{arquivo_principal}"
        )

    if not os.path.exists(
        arquivo_novo
    ):
        raise FileNotFoundError(
            f"Arquivo não encontrado: "
            f"{arquivo_novo}"
        )

    with open(
        arquivo_principal,
        "r",
        encoding="utf-8"
    ) as f:

        base_data = json.load(f)

    with open(
        arquivo_novo,
        "r",
        encoding="utf-8"
    ) as f:

        novo_data = json.load(f)

    mapa_contextos = {}

    for exemplo in base_data.get(
        "data",
        []
    ):

        ctx = normalizar_texto(
            exemplo["context"]
        )

        mapa_contextos[ctx] = exemplo

    contador_novos_contextos = 0
    contador_novas_perguntas = 0

    for exemplo_novo in novo_data.get(
        "data",
        []
    ):

        ctx_novo = normalizar_texto(
            exemplo_novo["context"]
        )

        if ctx_novo in mapa_contextos:

            exemplo_existente = (
                mapa_contextos[ctx_novo]
            )

            ids_existentes = {
                qa["id"]
                for qa in exemplo_existente["qas"]
            }

            for qa_nova in exemplo_novo["qas"]:

                if (
                    qa_nova["id"]
                    in ids_existentes
                ):
                    qa_nova["id"] += "_dup"

                exemplo_existente[
                    "qas"
                ].append(qa_nova)

                contador_novas_perguntas += 1

        else:

            base_data["data"].append(
                exemplo_novo
            )

            mapa_contextos[
                ctx_novo
            ] = exemplo_novo

            contador_novos_contextos += 1

            contador_novas_perguntas += len(
                exemplo_novo["qas"]
            )

    with open(
        arquivo_saida,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            base_data,
            f,
            ensure_ascii=False,
            indent=2
        )

    return {
        "contextos_adicionados":
        contador_novos_contextos,

        "perguntas_adicionadas":
        contador_novas_perguntas,

        "arquivo_saida":
        arquivo_saida
    }