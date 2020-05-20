import json

from django.conf import settings
from django.test import TestCase
from django.core.files import File

# Create your tests here.
from feedback.models import Feedback, TestFeedback
from problemas.models import Problema, Caso
from NiñasProject.utils import get_ordered_test_feedback
from usuarios.models import User


class problemasTest(TestCase):
    def setUp(self):
        script_path = settings.MEDIA_ROOT + '/test/watermelon.cpp'
        f = open(script_path)
        self.problema = Problema.objects.create(titulo="Problema de prueba")
        with open( settings.MEDIA_ROOT + '/test/casos_test.json', 'r') as archivo:
            datastore = json.load(archivo)

        for test_dict in datastore:  # Aquí es donde se generan los test, tengo que modificar para que reciba mi nueva info.
            caso = Caso(descripcion=test_dict["Descripcion"], input=test_dict["Input"],
                        output_esperado=test_dict["Output"], problema=self.problema)
            caso.save()
        archivo.close()
        self.usuaria_alumna = User.objects.create_user(username="alumna", password="contraseña123", es_alumna=True)
        self.feedback = Feedback.objects.create(user=self.usuaria_alumna, problema=self.problema,codigo_solucion=File(f))
        f.close()
        feedback_array = [[1, '1', 'NO', 'hola0', 0, 'NO'], [1, '2', 'NO', 'hola0', 0, 'NO'],
                          [1, '3', 'NO', 'hola0', 0, 'NO'], [1, '4', 'YES', 'hola0', 0, 'YES'],
                          [1, '5', 'NO', 'hola0', 0, 'NO'], [1, '6', 'YES', 'hola0', 0, 'YES'],
                          [1, '7', 'NO', 'hola0', 0, 'NO'], [1, '8', 'YES', 'hola0', 0, 'YES'],
                          [1, '9', 'NO', 'hola0', 0, 'NO'], [1, '10', 'YES', 'hola1', 0, 'YES'],
                          [1, '11', 'NO', 'hola1', 0, 'NO'], [1, '12', 'YES', 'hola1', 0, 'YES'],
                          [1, '13', 'NO', 'hola1', 0, 'NO'], [1, '14', 'YES', 'hola1', 0, 'YES'],
                          [1, '15', 'NO', 'hola1', 0, 'NO'], [1, '16', 'YES', 'hola1', 0, 'YES'],
                          [1, '17', 'NO', 'hola1', 0, 'NO'], [1, '18', 'YES', 'hola1', 0, 'YES'],
                          [1, '19', 'NO', 'hola1', 0, 'NO'], [1, '20', 'YES', 'hola2', 0, 'YES'],
                          [1, '21', 'NO', 'hola2', 0, 'NO'], [1, '22', 'YES', 'hola2', 0, 'YES'],
                          [1, '23', 'NO', 'hola2', 0, 'NO'], [1, '24', 'YES', 'hola2', 0, 'YES'],
                          [1, '25', 'NO', 'hola2', 0, 'NO'], [1, '26', 'YES', 'hola2', 0, 'YES'],
                          [1, '27', 'NO', 'hola2', 0, 'NO'], [1, '28', 'YES', 'hola2', 0, 'YES'],
                          [1, '29', 'NO', 'hola2', 0, 'NO'], [1, '30', 'YES', 'hola3', 0, 'YES'],
                          [1, '31', 'NO', 'hola3', 0, 'NO'], [1, '32', 'YES', 'hola3', 0, 'YES'],
                          [1, '33', 'NO', 'hola3', 0, 'NO'], [1, '34', 'YES', 'hola3', 0, 'YES'],
                          [1, '35', 'NO', 'hola3', 0, 'NO'], [1, '36', 'YES', 'hola3', 0, 'YES'],
                          [1, '37', 'NO', 'hola3', 0, 'NO'], [1, '38', 'YES', 'hola3', 0, 'YES'],
                          [1, '39', 'NO', 'hola3', 0, 'NO'], [1, '40', 'YES', 'hola4', 0, 'YES'],
                          [1, '41', 'NO', 'hola4', 0, 'NO'], [1, '42', 'YES', 'hola4', 0, 'YES'],
                          [1, '43', 'NO', 'hola4', 0, 'NO'], [1, '44', 'YES', 'hola4', 0, 'YES'],
                          [1, '45', 'NO', 'hola4', 0, 'NO'], [1, '46', 'YES', 'hola4', 0, 'YES'],
                          [1, '47', 'NO', 'hola4', 0, 'NO'], [1, '48', 'YES', 'hola4', 0, 'YES'],
                          [1, '49', 'NO', 'hola4', 0, 'NO']]



        for test in feedback_array:
            input = test[1]
            caso=Caso.objects.get(input=input,problema=self.problema)
            TestFeedback.objects.create(passed=test[0],output_obtenido=test[5],error=test[4],caso=caso,feedback=self.feedback)

    def test_get_ordered_test_feedback(self):
        '''
        La forma deberia ser
            [{descripcion:des, test_feedback:listadetest, casos_buenos:int, casos_malos: int},
            {descripcion:des, test_feedback:listadetest}, casos_buenos: int, casos_malos:int}

            ...
            ]
        :return:
        '''
        test_feedbacks = TestFeedback.objects.filter(feedback=self.feedback)
        result = get_ordered_test_feedback(test_feedbacks,self.problema)
        self.assertEqual(len(result),5)
        self.assertEqual(len(result[0]['test_feedback']),9)
