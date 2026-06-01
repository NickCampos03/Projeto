def criar_exemplo_squad(contexto, pergunta, resposta):

    if resposta:
        answer_start = contexto.find(resposta)

        if answer_start == -1:
            raise ValueError(
                "A resposta não foi encontrada dentro do contexto."
            )

        exemplo = {
            "context": contexto,
            "qas": [
                {
                    "id": f"id_{hash(pergunta)}",
                    "question": pergunta,
                    "is_impossible": False,
                    "answers": [
                        {
                            "text": resposta,
                            "answer_start": answer_start
                        }
                    ],
                    "plausible_answers": []
                }
            ]
        }

    else:
        exemplo = {
            "context": contexto,
            "qas": [
                {
                    "id": f"id_{hash(pergunta)}",
                    "question": pergunta,
                    "is_impossible": True,
                    "answers": [],
                    "plausible_answers": []
                }
            ]
        }

    return exemplo


def adicionar_exemplo(dataset, exemplo):
    dataset["data"].append(exemplo)