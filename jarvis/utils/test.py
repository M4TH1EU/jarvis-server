from padatious import IntentContainer

container = IntentContainer('intent_cache')

container.add_intent('spotify',
                     ["Joue {song} sur spotify",
                      "Joue {song}",
                      "Joue {song} (de|des|du groupe|du chanteur|de la chanteuse) {singer}",
                      "Mets la chanson {song} (de|des|du groupe|du chanteur|de la chanteuse) {singer}",
                      "Mets la chanson {song} (de|des|du groupe|du chanteur|de la chanteuse) {singer} sur spotify",
                      "Mets le titre {song}",
                      "Mets le titre {song} sur spotify",
                      "Mets le morceau {song}",
                      "Mets le morceau {song} sur spotify",
                      "Joue le morceau {song}",
                      "Joue le morceau {song} sur spotify",
                      "Mets le titre {song} (de|des|du groupe|du chanteur|de la chanteuse) {singer}",
                      "Mets le titre {song} (de|des|du groupe|du chanteur|de la chanteuse) {singer} sur spotify",
                      "Joue {song} (de|des|du groupe|du chanteur|de la chanteuse) {singer} sur spotify",
                      "Joue {song} (de|des|du groupe|du chanteur|de la chanteuse) {singer}",
                      "Joue le morceau {song} (de|des|du groupe|du chanteur|de la chanteuse) {singer}"
                      "Joue le morceau {song} (de|des|du groupe|du chanteur|de la chanteuse) {singer} sur spotify"
                      "Mets voir {song}",
                      "Mets voir {song} sur spotify",
                      "Mets voir {song} (de|des|du groupe|du chanteur|de la chanteuse) {singer}",
                      "Mets voir {song} (de|des|du groupe|du chanteur|de la chanteuse) {singer} sur spotify",
                      "Fait moi écouter {song}"
                      "Fait moi écouter {song} sur spotify"
                      "Fait moi écouter {song} (de|des|du groupe|du chanteur|de la chanteuse) {singer}"
                      "Fait moi écouter {song} (de|des|du groupe|du chanteur|de la chanteuse) {singer} sur spotify"
                      ])

container.train()

tests = ["joue time after time sur spotify",
         "mets le morceau fortunate son sur spotify",
         "joue le morceau crazy crazy nights",
         "mets voir crazy crazy nights",
         "mets la chanson crazy crazy nights de KISS",
         "fait moi écouter bye bye miss american pie",
         "joue le morceau bye bye miss american pie",
         "joue le morceau bye bye miss american pie du groupe billy cassidy",
         "joue hooked on a feeling sur spotify",
         "joue le morceau fortunate son de Willy and the Boys sur spotify"]

for test in tests:
    print("Sentence : " + test)

    result = container.calc_intent(test)
    if 'song' in result.matches:
        print("Song : " + result.matches.get('song'))

    if 'singer' in result.matches:
        print("Singer/Group : " + result.matches.get('singer'))

    print("")
    print("")
