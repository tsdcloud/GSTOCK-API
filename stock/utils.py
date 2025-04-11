from datetime import datetime


def generate_unique_num_ref(model):
    # NUM_REF peut être défini dynamiquement ou statiquement en fonction de vos besoins
    NUM_REF = 10001
    # Obtenez le mois/année actuel au format MM/YYYY
    codefin = datetime.now().strftime("%m/%Y")
    # Comptez le nombre d'objets avec une num_ref se terminant par le codefin actuel
    count = model.objects.filter(reference_number__endswith=codefin).count()
    # Calculez le nouvel ID en ajoutant le nombre d'objets actuels à NUM_REF
    new_id = NUM_REF + count
    # Concaténez le nouvel ID avec le codefin pour former la nouvelle num_ref
    concatenated_num_ref = f"{new_id}/{codefin}"
    # concatenated_num_ref = str(new_id) + "/" + str(codefin) #f"{new_id}/{codefin}"
    return concatenated_num_ref

def unique_reference_number_generator(model):
    last_ref = model.objects.order_by('-id').first()

    if last_ref and last_ref.reference_number.startswith("REF"):
        last_number = int(last_ref.reference_number[3:])
        reference_number = f"REF{last_number + 1:04d}"
    else:
        reference_number = "REF0001"

    # Vérifier si la référence existe déjà et générer une nouvelle si nécessaire
    if model.objects.filter(reference_number=reference_number).exists():
        last_number += 1
        
    reference_number = f"REF{last_number:04d}"

    return reference_number