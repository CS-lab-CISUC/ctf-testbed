from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/create-vms", methods=["POST"])
def create_vms():
    data = request.get_json()
    print("Im alive")
    if not data or not isinstance(data, list):
        return jsonify({"error": "Formato inválido. Esperada uma lista de challenges."}), 400

    created_vms = []

    for challenge in data:
        name = challenge.get("name")
        template_uuid = challenge.get("template_uuid")
        network_uuid = challenge.get("network_uuid")

        if template_uuid and network_uuid:
            print(f" Criar VM para challenge '{name}' com template '{template_uuid}' e rede '{network_uuid}'")

            created_vms.append({
                "challenge": name,
                "template_uuid": template_uuid,
                "network_uuid": network_uuid,
                "status": "VM criada (simulado)"
            })
        else:
            print(f"ℹ Challenge '{name}' não requer VM.")

    return jsonify({
        "status": "Processamento completo",
        "vms_criadas": created_vms,
        "total": len(created_vms)
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
