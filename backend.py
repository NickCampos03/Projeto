import uuid

def criar_exemplo_squad(contexto, pergunta, resposta=None):
    if resposta:
        answer_start = contexto.find(resposta)

        if answer_start == -1:
            raise ValueError("Resposta não encontrada no contexto!")

        answers = [{
            "text": resposta,
            "answer_start": answer_start
        }]
        is_impossible = False
    else:
        answers = []
        is_impossible = True

    exemplo = {
        "data": [
            {
                "title": "exemplo",
                "paragraphs": [
                    {
                        "context": contexto,
                        "qas": [
                            {
                                "id": str(uuid.uuid4()),
                                "question": pergunta,
                                "answers": answers,
                                "is_impossible": is_impossible
                            }
                        ]
                    }
                ]
            }
        ]
    }

    return exemplo


def adicionar_exemplo(dataset, exemplo):
    dataset["data"].extend(exemplo["data"])