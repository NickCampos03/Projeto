import json
import os


def criar_exemplo_squad(
    titulo_tema,
    contexto,
    pergunta,
    resposta="",
    is_impossible=False,
    id_contador=1
):

    qa_dict = {
        "id": f"id_{titulo_tema}_{id_contador}",
        "question": pergunta,
        "is_impossible": is_impossible,
        "answers": [],
        "plausible_answers": []
    }

    if not is_impossible:

        answer_start = contexto.find(resposta)

        if answer_start == -1:
            raise ValueError(
                "A resposta não foi encontrada exatamente no contexto."
            )

        qa_dict["answers"].append({
            "text": resposta,
            "answer_start": answer_start
        })

    return {
        "context": contexto,
        "qas": [qa_dict]
    }


def adicionar_exemplo(dataset, titulo_tema, exemplo):

    if not dataset["data"]:

        dataset["data"].append({
            "title": titulo_tema,
            "paragraphs": []
        })

    dataset["data"][0]["paragraphs"].append(exemplo)


def normalizar_texto(texto):
    return " ".join(texto.strip().lower().split())


def salvar_dataset(dataset, nome_arquivo):

    if not nome_arquivo.endswith(".json"):
        nome_arquivo += ".json"

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(
            dataset,
            f,
            ensure_ascii=False,
            indent=2
        )

    return os.path.abspath(nome_arquivo)


def fazer_merge_squad(
    arquivo_principal,
    arquivo_novo,
    arquivo_saida
):

    if not os.path.exists(arquivo_principal):
        raise FileNotFoundError(
            f"Arquivo não encontrado: {arquivo_principal}"
        )

    if not os.path.exists(arquivo_novo):
        raise FileNotFoundError(
            f"Arquivo não encontrado: {arquivo_novo}"
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

    for topico in base_data.get("data", []):

        for paragrafo in topico.get(
            "paragraphs",
            []
        ):

            ctx = normalizar_texto(
                paragrafo["context"]
            )

            mapa_contextos[ctx] = paragrafo

    if not base_data.get("data"):

        base_data["data"] = [{
            "title": "Dataset_Merged",
            "paragraphs": []
        }]

    alvo_topico = base_data["data"][0]

    for topico_novo in novo_data.get(
        "data",
        []
    ):

        for paragrafo_novo in topico_novo.get(
            "paragraphs",
            []
        ):

            ctx_novo = normalizar_texto(
                paragrafo_novo["context"]
            )

            if ctx_novo in mapa_contextos:

                existente = mapa_contextos[ctx_novo]

                ids_existentes = {
                    qa["id"]
                    for qa in existente["qas"]
                }

                for qa_nova in paragrafo_novo["qas"]:

                    if qa_nova["id"] in ids_existentes:

                        qa_nova["id"] += "_dup"

                    existente["qas"].append(
                        qa_nova
                    )

            else:

                alvo_topico["paragraphs"].append(
                    paragrafo_novo
                )

                mapa_contextos[
                    ctx_novo
                ] = paragrafo_novo

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

    return arquivo_saida