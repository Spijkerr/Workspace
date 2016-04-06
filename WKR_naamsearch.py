import unittest

class TestStringMethods(unittest.TestCase):
    def test_known_surname_search1(self):
        #Controleert of de voornaam inderdaad wordt herkend.
        name = "Bankstel Offerman"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertEqual(results[0].group('surname'), 'Offerman', "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('firstname'), "Bankstel", "Gevonden voornaam matcht niet met input")
                
        self.NameDet.clear_results()
		
    def test_known_surname_search2(self):
        #Controleert of de voornaam inderdaad wordt herkend. Met achternaam eerst.
        name = "Offerman, Bankstel"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertEqual(results[0].group('surname'), 'Offerman', "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('firstname'), "Bankstel", "Gevonden voornaam matcht niet met input")
                
        self.NameDet.clear_results()
		
    def test_known_surname_search3(self):
        #Controleert of de achternaam gevolgd met punt inderdaad niet wordt herkend.
        name = "Bankstel Offerman."
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertFalse(results, "Toch een achternaam gevonden")
        
                
        self.NameDet.clear_results()
		
    def test_known_surname_search4(self):
        #Controleert of de voornaam inderdaad wordt herkend inclusief overbodige spaties.
        name = "Bankstel   Offerman "
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertEqual(results[0].group('surname'), 'Offerman', "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('firstname'), "Bankstel", "Gevonden voornaam matcht niet met input")
                
        self.NameDet.clear_results()
		
    def test_known_surname_search5(self):
        #Controleert of de voornaam inderdaad wordt herkend inclusief overbodige komma's.
        name = "Bankstel, Offerman,"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertEqual(results[0].group('surname'), 'Offerman', "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('firstname'), "Bankstel", "Gevonden voornaam matcht niet met input")
                
        self.NameDet.clear_results()

    def test_known_surname_search6(self):
        #Controleert of de achternaam met kleine letters inderdaad niet herkend wordt.
        name = "Bankstel offerman"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertFalse(results, "Toch een achternaam gevonden")
		
        self.NameDet.clear_results()
		
    def test_known_surname_search7(self):
        #Controleert of de voornaam met kleine letters inderdaad niet herkend wordt.
        name = "bankstel Offerman"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertEqual(results[0].group('surname'), 'Offerman', "Gevonden achternaam matcht niet met input")
        self.assertFalse(results[0].group('firstname'), "Bankstel", "Gevonden voornaam matcht niet met input")
		
        self.NameDet.clear_results()
		
    def test_known_surname_search8(self):
        #Controleert of er een dubbele voornaam wordt herkend.
        name = "Bankstel Koek Offerman"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertEqual(results[0].group('surname'), 'Offerman', "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('firstname'), "Bankstel Koek", "Gevonden voornaam matcht niet met input")
		
        self.NameDet.clear_results()
		
    def test_known_surname_search9(self):
        #Controleert of er een titel wordt herkend.
        name = "Dhr Bankstel Offerman"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertEqual(results[0].group('surname'), 'Offerman', "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('firstname'), "Bankstel Koek", "Gevonden voornaam matcht niet met input")
        self.assertEqual(results[0].group('title'), "Dhr" , "Gevonden titel matcht niet met input")
		
        self.NameDet.clear_results()
		
    def test_known_surname_search10(self):
        #Controleert of er een titel wordt herkend op een complexere manier
        name = "Dhr, Offerman, Bankstel"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertEqual(results[0].group('surname'), 'Offerman', "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('firstname'), "Bankstel Koek", "Gevonden voornaam matcht niet met input")
        self.assertEqual(results[0].group('title'), "Dhr," , "Gevonden titel matcht niet met input")
		
        self.NameDet.clear_results()
		
    def test_known_surname_search11(self):
        #Controleert of er inderdaad geen titel wordt herkend met een punt.
        name = "Dhr. Bankstel Offerman"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertEqual(results[0].group('surname'), 'Offerman', "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('firstname'), "Bankstel Koek", "Gevonden voornaam matcht niet met input")
        self.assertFalse(results[0].group('title'), "Dhr." , "Gevonden titel matcht niet met input")
		
        self.NameDet.clear_results()
		
    def test_known_surname_search12(self):
        #Controleert of de voornaam inderdaad niet wordt herkend met onzin ertussen.
        name = "Bankstel sptprpe Offerman"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertEqual(results[0].group('surname'), 'Offerman', "Gevonden achternaam matcht niet met input")
        self.assertFalse(results[0].group('firstname'), "Bankstel", "Gevonden voornaam matcht niet met input")
                
        self.NameDet.clear_results()
		
    def test_known_firstname_search1(self):
        #Controleert of de achternaam inderdaad wordt herkend.
        name = "Thomas Stoelendans"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertEqual(results[0].group('surname'), 'Stoelendans', "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('firstname'), "Thomas", "Gevonden voornaam matcht niet met input")
                
        self.NameDet.clear_results()
		
    def test_known_firstname_search2(self):
        #Controleert of de achternaam inderdaad wordt herkend. Met achternaam eerst.
        name = "Stoelendans, Thomas"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertEqual(results[0].group('surname'), 'Stoelendans', "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('firstname'), "Thomas", "Gevonden voornaam matcht niet met input")
                
        self.NameDet.clear_results()
		
    def test_known_firstname_search3(self):
        #Controleert of de voornaam gevolgd met punt inderdaad niet wordt herkend.
        name = "Thomas. Stoelendans"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertFalse(results, "Toch een achternaam gevonden")
        
                
        self.NameDet.clear_results()
		
    def test_known_firstname_search4(self):
        #Controleert of de achternaam inderdaad wordt herkend inclusief overbodige spaties.
        name = "Thomas   Stoelendans "
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertEqual(results[0].group('surname'), 'Stoelendans', "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('firstname'), "Thomas", "Gevonden voornaam matcht niet met input")
                
        self.NameDet.clear_results()
		
    def test_known_firstname_search5(self):
        #Controleert of de achternaam inderdaad wordt herkend inclusief overbodige komma's.
        name = "Thomas, Offerman,"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertEqual(results[0].group('surname'), 'Stoelendans', "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('firstname'), "Thomas", "Gevonden voornaam matcht niet met input")
                
        self.NameDet.clear_results()

    def test_known_firstname_search6(self):
        #Controleert of de voornaam met kleine letters inderdaad niet herkend wordt.
        name = "thomas offerman"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertFalse(results, "Toch een achternaam gevonden")
		
        self.NameDet.clear_results()
		
    def test_known_firstname_search7(self):
        #Controleert of de achternaam met kleine letters inderdaad niet herkend wordt.
        name = "Thomas stoelendans"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertFalse(results[0].group('surname'), 'stoelendans', "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('firstname'), "Thomas", "Gevonden voornaam matcht niet met input")
		
        self.NameDet.clear_results()
		
    def test_known_firstname_search8(self):
        #Controleert of er een dubbele achternaam wordt herkend.
        name = "Thomas Koek Stoelendans"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertEqual(results[0].group('surname'), 'Koek Stoelendans', "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('firstname'), "Thomas", "Gevonden voornaam matcht niet met input")
		
        self.NameDet.clear_results()
		
    def test_known_firstname_search9(self):
        #Controleert of er een titel wordt herkend.
        name = "Dhr Thomas Stoelendans"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertEqual(results[0].group('surname'), 'Offerman', "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('firstname'), "Bankstel Koek", "Gevonden voornaam matcht niet met input")
        self.assertEqual(results[0].group('title'), "Dhr" , "Gevonden titel matcht niet met input")
		
        self.NameDet.clear_results()
		
    def test_known_firstname_search10(self):
        #Controleert of er een titel wordt herkend op een complexere manier
        name = "Dhr, Stoelendans, Thomas"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertEqual(results[0].group('surname'), 'Offerman', "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('firstname'), "Bankstel Koek", "Gevonden voornaam matcht niet met input")
        self.assertEqual(results[0].group('title'), "Dhr," , "Gevonden titel matcht niet met input")
		
        self.NameDet.clear_results()
		
    def test_known_firstname_search11(self):
        #Controleert of er inderdaad geen titel wordt herkend als er een punt achter staat.
        name = "Dhr. Thomas Stoelendans"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertEqual(results[0].group('surname'), 'Offerman', "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('firstname'), "Bankstel Koek", "Gevonden voornaam matcht niet met input")
        self.assertEqual(results[0].group('title'), "Dhr." , "Gevonden titel matcht niet met input")
		
        self.NameDet.clear_results()
		
    def test_known_firstname_search12(self):
        #Controleert of de achternaam inderdaad niet wordt herkend met onzin ertussen.
        name = "Thomas sprorsp Stoelendans"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertFalse(results[0].group('surname'), 'Stoelendans', "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('firstname'), "Thomas", "Gevonden voornaam matcht niet met input")
                
        self.NameDet.clear_results()
		
    def test_known_prefix_1(self):
        #Controleren of de naam ook wordt herkend door middel van een tussenvoegsel.
        name = "Bankstel van der Stoelendans"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertEqual(results[0].group('surname'), 'Bankstel' "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('initials'), "Stoelendans", "Gevonden initialen matcht niet met input")
        self.assertEqual(results[0].group('prefix'), "van der", "Gevonden tussenvoegsel matcht niet met input")
                
        self.NameDet.clear_results()
		
    def test_known_prefix_2(self):
        #Controleren of de naam ook wordt herkend door middel van een tussenvoegsel met extra spaties
        name = "Bankstel  van  der  Stoelendans"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertEqual(results[0].group('surname'), 'Bankstel' "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('initials'), "Stoelendans", "Gevonden initialen matcht niet met input")
        self.assertEqual(results[0].group('prefix'), "van der", "Gevonden tussenvoegsel matcht niet met input")
                
        self.NameDet.clear_results()
		
    def test_known_prefix_3(self):
        #Controleren of de naam ook wordt herkend door middel van een tussenvoegsel met komma's.
        name = "Bankstel, van der Stoelendans"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertEqual(results[0].group('surname'), 'Bankstel' "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('initials'), "Stoelendans", "Gevonden initialen matcht niet met input")
        self.assertEqual(results[0].group('prefix'), "van der", "Gevonden tussenvoegsel matcht niet met input")
                
        self.NameDet.clear_results()
		
    def test_known_prefix_4(self):
        #Controleren of de prefix niet wordt gepakt met punten ertussen.
        name = "Bankstel van. der Stoelendans"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertFalse(results)

                
        self.NameDet.clear_results()
		
    def test_known_prefix_5(self):
        #Controleren of de prefix niet wordt gepakt met hoofdletters.
        name = "Bankstel Van Der Stoelendans"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertFalse(results)

                
        self.NameDet.clear_results()
		
    def test_known_title_1(self):
        #Controleren of een titel een achternaam vindt.
        name = "Dhr Stoelendans"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertEqual(results[0].group('surname'), 'Stoelendans', "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('title'), "Dhr", "Gevonden titel matcht niet met input")

        self.NameDet.clear_results()
		
    def test_known_title_2(self):
        #Controleren of een titel met kommas een achternaam vindt.
        name = "Dhr, Stoelendans"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertEqual(results[0].group('surname'), 'Stoelendans', "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('title'), "Dhr,", "Gevonden titel matcht niet met input")

        self.NameDet.clear_results()
		
    def test_known_title_3(self):
        #Controleren of een titel met een punt erachter inderdaad niks vindt.
        name = "Dhr. Stoelendans"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertFalse(results)


        self.NameDet.clear_results()
	
    def test_known_title_4(self):
        #Controleren of de titel MsC een achternaam vindt.
        name = "MsC Stoelendans"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertEqual(results[0].group('surname'), 'Stoelendans', "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('title'), "Dhr", "Gevonden titel matcht niet met input")

        self.NameDet.clear_results()
		
    def test_known_title_5(self):
        #Controleren of de titel Mw, een achternaam vindt.
        name = "Mw,  Kippenhok"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertEqual(results[0].group('surname'), 'Kippenhok', "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('title'), "Dhr", "Gevonden titel matcht niet met input")

        self.NameDet.clear_results()
		
    def test_known_title_6(self):
        #Controleren of de titel Mw, geen achternaam vindt als deze met kleine letters is geschreven
        name = "Mw,  kippenhok"
        string = "Random FFF00F osos--os String test " + name + " blabla Hossel ddooo -- s-s"
        self.NameDet.parse_string(string)
        results = self.NameDet.return_results()
        self.assertTrue(results)
        self.assertFalse(results[0].group('surname'), 'Kippenhok', "Gevonden achternaam matcht niet met input")
        self.assertEqual(results[0].group('title'), "Dhr", "Gevonden titel matcht niet met input")

        self.NameDet.clear_results()
        
suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
unittest.TextTestRunner(verbosity=2).run(suite)
		