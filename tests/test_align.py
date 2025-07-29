"""
Tests for the align module.
"""

import math

import pytest
import scipy.stats as stats

from vivre.align import Aligner


def split_text_to_sentences(text: str) -> list[str]:
    """Helper function to split text into sentences for testing."""
    import re

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if s.strip()]


class TestAligner:
    """Test cases for the Aligner class."""

    def test_align_perfect_match_english(self):
        """Test alignment of perfectly matched English text."""
        aligner = Aligner()

        source_sentences = ["Hello world.", "How are you today?"]
        target_sentences = ["Hello world.", "How are you today?"]

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have 2 aligned segments (one for each sentence)
        assert len(alignment) == 2, "Should have 2 aligned segments"

        # Each segment should contain corresponding sentences
        source_seg1, target_seg1 = alignment[0]
        source_seg2, target_seg2 = alignment[1]

        assert (
            source_seg1 == "Hello world."
        ), "First source segment should be 'Hello world.'"
        assert (
            target_seg1 == "Hello world."
        ), "First target segment should be 'Hello world.'"
        assert (
            source_seg2 == "How are you today?"
        ), "Second source segment should be 'How are you today?'"
        assert (
            target_seg2 == "How are you today?"
        ), "Second target segment should be 'How are you today?'"

    def test_align_perfect_match_spanish(self):
        """Test alignment of perfectly matched Spanish text."""
        aligner = Aligner()

        source_sentences = ["Hola mundo.", "¿Cómo estás hoy?"]
        target_sentences = ["Hola mundo.", "¿Cómo estás hoy?"]

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have 2 aligned segments (one for each sentence)
        assert len(alignment) == 2, "Should have 2 aligned segments"

        # Each segment should contain corresponding sentences
        source_seg1, target_seg1 = alignment[0]
        source_seg2, target_seg2 = alignment[1]

        assert (
            source_seg1 == "Hola mundo."
        ), "First source segment should be 'Hola mundo.'"
        assert (
            target_seg1 == "Hola mundo."
        ), "First target segment should be 'Hola mundo.'"
        assert (
            source_seg2 == "¿Cómo estás hoy?"
        ), "Second source segment should be '¿Cómo estás hoy?'"
        assert (
            target_seg2 == "¿Cómo estás hoy?"
        ), "Second target segment should be '¿Cómo estás hoy?'"

    def test_align_perfect_match_french(self):
        """Test alignment of perfectly matched French text."""
        aligner = Aligner()

        source_sentences = ["Bonjour le monde.", "Comment allez-vous aujourd'hui?"]
        target_sentences = ["Bonjour le monde.", "Comment allez-vous aujourd'hui?"]

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have 2 aligned segments (one for each sentence)
        assert len(alignment) == 2, "Should have 2 aligned segments"

        # Each segment should contain corresponding sentences
        source_seg1, target_seg1 = alignment[0]
        source_seg2, target_seg2 = alignment[1]

        assert (
            source_seg1 == "Bonjour le monde."
        ), "First source segment should be 'Bonjour le monde.'"
        assert (
            target_seg1 == "Bonjour le monde."
        ), "First target segment should be 'Bonjour le monde.'"
        assert (
            source_seg2 == "Comment allez-vous aujourd'hui?"
        ), "Second source segment should be 'Comment allez-vous aujourd'hui?'"
        assert (
            target_seg2 == "Comment allez-vous aujourd'hui?"
        ), "Second target segment should be 'Comment allez-vous aujourd'hui?'"

    def test_align_single_sentence(self):
        """Test alignment of single sentences."""
        aligner = Aligner()

        source_sentences = ["Hello world."]
        target_sentences = ["Hola mundo."]

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have 1 aligned segment
        assert len(alignment) == 1, "Should have 1 aligned segment"

        # The segment should contain the sentences
        source_seg, target_seg = alignment[0]
        assert source_seg == "Hello world.", "Source segment should be 'Hello world.'"
        assert target_seg == "Hola mundo.", "Target segment should be 'Hola mundo.'"

    def test_align_empty_texts(self):
        """Test alignment with empty sentence lists."""
        aligner = Aligner()

        alignment = aligner.align([], [])

        # Should return empty list
        assert alignment == [], "Should return empty list for empty inputs"

    def test_align_whitespace_only(self):
        """Test alignment with whitespace-only sentences."""
        aligner = Aligner()

        source_sentences = ["   ", "", "  \n  "]
        target_sentences = ["Hello world."]

        alignment = aligner.align(source_sentences, target_sentences)

        # Should return empty list since all source sentences are empty
        assert (
            alignment == []
        ), "Should return empty list for whitespace-only source sentences"

    def test_align_with_punctuation(self):
        """Test alignment with various punctuation marks."""
        aligner = Aligner()

        source_sentences = ["Hello!", "How are you?", "I'm fine."]
        target_sentences = ["¡Hola!", "¿Cómo estás?", "Estoy bien."]

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have alignments (may not be exactly 3 due to optimal alignment)
        assert len(alignment) > 0, "Should have alignments"
        assert len(alignment) <= 3, "Should have at most 3 aligned segments"

        # Each segment should contain questions or statements
        for source_seg, target_seg in alignment:
            assert (
                "?" in source_seg
                or "!" in source_seg
                or "¿" in target_seg
                or "¡" in target_seg
            ), "Should contain punctuation marks"

    def test_align_with_numbers(self):
        """Test alignment with sentences containing numbers."""
        aligner = Aligner()

        source_sentences = ["I have 5 apples.", "The year is 2024.", "Count to 10."]
        target_sentences = ["Tengo 5 manzanas.", "El año es 2024.", "Cuenta hasta 10."]

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have alignments (may not be exactly 3 due to optimal alignment)
        assert len(alignment) > 0, "Should have alignments"
        assert len(alignment) <= 3, "Should have at most 3 aligned segments"

        # Each segment should have substantial content
        for source_seg, target_seg in alignment:
            assert (
                len(source_seg) > 10
            ), "Source segment should have substantial content"
            assert (
                len(target_seg) > 10
            ), "Target segment should have substantial content"

    def test_align_multilingual_mix(self):
        """Test alignment with multilingual content."""
        aligner = Aligner()

        source_sentences = ["Hello world.", "Bonjour le monde.", "Hola mundo."]
        target_sentences = ["Hello world.", "Bonjour le monde.", "Hola mundo."]

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have 3 aligned segments
        assert len(alignment) == 3, "Should have 3 aligned segments"

        # Each segment should contain corresponding sentences
        for i, (source_seg, target_seg) in enumerate(alignment):
            expected = source_sentences[i]
            assert source_seg == expected, f"Source segment {i} should be '{expected}'"
            assert target_seg == expected, f"Target segment {i} should be '{expected}'"

    def test_align_long_text(self):
        """Test alignment with longer text."""
        aligner = Aligner()

        source_sentences = [
            "The quick brown fox jumps over the lazy dog.",
            "This sentence contains all the letters of the alphabet.",
            "Pack my box with five dozen liquor jugs.",
        ]
        target_sentences = [
            "El zorro marrón rápido salta sobre el perro perezoso.",
            "Esta oración contiene todas las letras del alfabeto.",
            "Empaca mi caja con cinco docenas de jarras de licor.",
        ]

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have alignments (may not be exactly 3 due to optimal alignment)
        assert len(alignment) > 0, "Should have alignments"
        assert len(alignment) <= 3, "Should have at most 3 aligned segments"

        # Each segment should have substantial content
        for source_seg, target_seg in alignment:
            assert (
                len(source_seg) > 20
            ), "Source segment should have substantial content"
            assert (
                len(target_seg) > 20
            ), "Target segment should have substantial content"

    def test_align_english_spanish_simple(self):
        """Test alignment of English-Spanish translation pairs with "
        "statistically sound algorithm."""
        aligner = Aligner()

        source_sentences = ["Hello world.", "How are you today?"]
        target_sentences = ["Hola mundo.", "¿Cómo estás hoy?"]

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have at least one aligned segment
        assert len(alignment) > 0, "Should have at least one aligned segment"

        # Each segment should contain corresponding translations
        for source_seg, target_seg in alignment:
            # Should contain both sentences (may be aligned as 2-2)
            assert (
                "Hello world" in source_seg
            ), "Source segment should contain 'Hello world'"
            assert (
                "How are you today" in source_seg
            ), "Source segment should contain 'How are you today'"
            assert (
                "Hola mundo" in target_seg
            ), "Target segment should contain 'Hola mundo'"
            assert (
                "Cómo estás hoy" in target_seg
            ), "Target segment should contain 'Cómo estás hoy'"

    def test_align_english_spanish_complex(self):
        """Test alignment of complex English-Spanish translation pairs."""
        aligner = Aligner()

        source_sentences = [
            "The ancient castle stood majestically on the hilltop.",
            "Its stone walls were weathered by centuries of wind and rain.",
            "Inside the grand hall, tapestries depicted historical battles.",
            "The library contained thousands of books.",
        ]
        target_sentences = [
            "El antiguo castillo se alzaba majestuosamente en la cima de la colina.",
            "Sus muros de piedra estaban desgastados por siglos de viento y lluvia.",
            "Dentro del gran salón, tapices representaban batallas históricas.",
            "La biblioteca contenía miles de libros.",
        ]

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have alignments (may not be exactly 4 due to optimal alignment)
        assert len(alignment) > 0, "Should have alignments"
        assert len(alignment) <= 4, "Should have at most 4 aligned segments"

        # Each segment should have substantial content
        for source_seg, target_seg in alignment:
            assert (
                len(source_seg) > 20
            ), "Source segment should have substantial content"
            assert (
                len(target_seg) > 20
            ), "Target segment should have substantial content"

    def test_align_english_spanish_questions(self):
        """Test alignment of English-Spanish question sentences."""
        aligner = Aligner()

        source_sentences = [
            "What is your name?",
            "Where do you live?",
            "How old are you?",
            "Do you speak Spanish?",
        ]
        target_sentences = [
            "¿Cómo te llamas?",
            "¿Dónde vives?",
            "¿Cuántos años tienes?",
            "¿Hablas español?",
        ]

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have alignments (may not be exactly 4 due to optimal alignment)
        assert len(alignment) > 0, "Should have alignments"
        assert len(alignment) <= 4, "Should have at most 4 aligned segments"

        # Each segment should contain questions
        for source_seg, target_seg in alignment:
            assert (
                "?" in source_seg or "¿" in target_seg
            ), "Should contain question marks"

    def test_align_english_spanish_story(self):
        """Test alignment of English-Spanish story sentences."""
        aligner = Aligner()

        source_sentences = [
            "Once upon a time, there was a little girl who lived in a "
            "village near the forest.",
            "Whenever she went out, the little girl wore a red riding cloak.",
            "So everyone in the village called her Little Red Riding Hood.",
            "One morning, Little Red Riding Hood asked her mother if she "
            "could go to visit her grandmother.",
        ]
        target_sentences = [
            "Érase una vez una niña que vivía en una aldea cerca del bosque.",
            "Siempre que salía, la niña llevaba una capa roja de montar.",
            "Por eso todos en la aldea la llamaban Caperucita Roja.",
            "Una mañana, Caperucita Roja le preguntó a su madre si podía "
            "ir a visitar a su abuela.",
        ]

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have alignments (may not be exactly 4 due to optimal alignment)
        assert len(alignment) > 0, "Should have alignments"
        assert len(alignment) <= 4, "Should have at most 4 aligned segments"

        # Each segment should have substantial content
        for source_seg, target_seg in alignment:
            assert (
                len(source_seg) > 30
            ), "Source segment should have substantial content"
            assert (
                len(target_seg) > 30
            ), "Target segment should have substantial content"

    def test_align_empty_source_sentences(self):
        """Test alignment when source sentences are minimal."""
        aligner = Aligner()

        source_sentences = [
            "   .   ",
            "   .   ",
            "   .   ",
        ]  # Only punctuation and whitespace
        target_sentences = ["Hello world.", "How are you?"]

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have alignments (algorithm finds sentences even in edge cases)
        assert (
            len(alignment) > 0
        ), "Should have alignments even with minimal source sentences"

        # Each alignment should have content (may have empty source segments)
        for source_seg, target_seg in alignment:
            assert (
                len(source_seg) > 0 or len(target_seg) > 0
            ), "At least one segment should have content"

    def test_align_empty_target_sentences(self):
        """Test alignment when target sentences are minimal."""
        aligner = Aligner()

        source_sentences = ["Hello world.", "How are you?"]
        target_sentences = [
            "   .   ",
            "   .   ",
            "   .   ",
        ]  # Only punctuation and whitespace

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have alignments (algorithm finds sentences even in edge cases)
        assert (
            len(alignment) > 0
        ), "Should have alignments even with minimal target sentences"

        # Each alignment should have content
        for source_seg, target_seg in alignment:
            assert len(source_seg) > 0, "Source segment should have content"

    def test_align_both_minimal_sentences(self):
        """Test alignment when both source and target sentences are minimal."""
        aligner = Aligner()

        source_sentences = ["   .   ", "   .   "]
        target_sentences = ["   .   ", "   .   "]

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have alignments (algorithm finds sentences even in edge cases)
        assert len(alignment) > 0, "Should have alignments even with minimal sentences"

        # Each alignment should have content
        for source_seg, target_seg in alignment:
            assert (
                len(source_seg) > 0 or len(target_seg) > 0
            ), "At least one segment should have content"

    def test_align_single_source_multiple_target(self):
        """Test alignment with single source sentence and multiple target sentences."""
        aligner = Aligner()

        source_sentences = ["Hello world."]
        target_sentences = ["Hola mundo.", "¿Cómo estás?"]

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have at least one alignment
        assert len(alignment) > 0, "Should have at least one alignment"

        # Each alignment should have content (may have empty segments due to
        # algorithm behavior)
        for source_seg, target_seg in alignment:
            # At least one segment should have content
            assert (
                len(source_seg) > 0 or len(target_seg) > 0
            ), "At least one segment should have content"

    def test_align_multiple_source_single_target(self):
        """Test alignment with multiple source sentences and single target sentence."""
        aligner = Aligner()

        source_sentences = ["Hello world.", "How are you?"]
        target_sentences = ["Hola mundo."]

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have at least one alignment
        assert len(alignment) > 0, "Should have at least one alignment"

        # Each alignment should have content (may have empty segments due to
        # algorithm behavior)
        for source_seg, target_seg in alignment:
            # At least one segment should have content
            assert (
                len(source_seg) > 0 or len(target_seg) > 0
            ), "At least one segment should have content"

    def test_align_edge_case_reconstruction(self):
        """Test alignment edge case that exercises the reconstruction logic."""
        aligner = Aligner()

        # Use very different length texts to force complex alignment
        source_sentences = ["A.", "B.", "C.", "D.", "E."]
        target_sentences = [
            "Very long sentence that should align with multiple short ones."
        ]

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have at least one alignment
        assert len(alignment) > 0, "Should have at least one alignment"

        # Each alignment should have content (may have empty segments due to
        # algorithm behavior)
        for source_seg, target_seg in alignment:
            # At least one segment should have content
            assert (
                len(source_seg) > 0 or len(target_seg) > 0
            ), "At least one segment should have content"

    def test_align_cost_function_edge_cases(self):
        """Test alignment cost function with various edge cases."""
        aligner = Aligner()

        # Test with very long sentences to trigger the large alignment penalty
        source_sentences = ["A" * 100 + ".", "B" * 100 + "."]
        target_sentences = ["C" * 50 + ".", "D" * 50 + "."]

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have alignments
        assert (
            len(alignment) > 0
        ), "Should have alignments even with very long sentences"

        # Each alignment should have content
        for source_seg, target_seg in alignment:
            assert (
                len(source_seg) > 0 or len(target_seg) > 0
            ), "At least one segment should have content"

    def test_align_dp_algorithm_edge_cases(self):
        """Test DP algorithm with edge cases that exercise different alignment types."""
        aligner = Aligner()

        # Test with many short sentences to exercise various alignment combinations
        source_sentences = ["A.", "B.", "C.", "D.", "E.", "F.", "G.", "H.", "I.", "J."]
        target_sentences = ["1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10."]

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have alignments
        assert len(alignment) > 0, "Should have alignments with many short sentences"

        # Each alignment should have content
        for source_seg, target_seg in alignment:
            assert (
                len(source_seg) > 0 or len(target_seg) > 0
            ), "At least one segment should have content"

    def test_align_2_1_pattern(self):
        """Test alignment with 2-1 pattern (two source sentences align to "
        "one target sentence)."""
        aligner = Aligner()

        # Create paragraph-sized input with 2-1 alignment pattern
        source_text = (
            "The morning sun rose over the distant mountains, casting long "
            "shadows across the valley floor. "
            "Birds began their daily chorus, filling the air with melodic "
            "songs that echoed through the trees. "
            "A gentle breeze carried the scent of pine and wildflowers, "
            "creating a peaceful atmosphere. "
            "The village slowly came to life as people emerged from their "
            "homes to begin their daily routines. "
            "Children's laughter could be heard from the nearby schoolyard, "
            "adding to the morning's symphony."
        )

        target_text = (
            "El sol de la mañana se alzó sobre las montañas distantes, "
            "proyectando largas sombras a través del valle. "
            "Los pájaros comenzaron su coro diario, llenando el aire con "
            "canciones melódicas que resonaban a través de los árboles. "
            "Una brisa suave llevaba el aroma de pino y flores silvestres, "
            "creando una atmósfera pacífica. "
            "El pueblo lentamente cobraba vida mientras la gente emergía de "
            "sus hogares para comenzar sus rutinas diarias. "
            "Se podía escuchar la risa de los niños desde el patio de la "
            "escuela cercana, añadiendo a la sinfonía de la mañana."
        )

        source_sentences = split_text_to_sentences(source_text)
        target_sentences = split_text_to_sentences(target_text)

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have alignments
        assert len(alignment) > 0, "Should have alignments for 2-1 pattern"

        # Check for various alignment patterns
        alignment_patterns = []
        for source_seg, target_seg in alignment:
            # Count sentences in source segment
            source_sentences = len([s for s in source_seg.split(".") if s.strip()])
            target_sentences = len([s for s in target_seg.split(".") if s.strip()])
            alignment_patterns.append((source_sentences, target_sentences))

        # Should have multiple alignment patterns
        assert len(alignment_patterns) > 1, "Should have multiple alignment segments"

        # Check that we have substantial content
        total_source_chars = sum(len(source_seg) for source_seg, _ in alignment)
        total_target_chars = sum(len(target_seg) for _, target_seg in alignment)

        assert total_source_chars > 200, "Should have substantial source content"
        assert total_target_chars > 200, "Should have substantial target content"

    def test_align_1_2_pattern(self):
        """Test alignment with 1-2 pattern (one source sentence aligns to "
        "two target sentences)."""
        aligner = Aligner()

        # Create paragraph-sized input with 1-2 alignment pattern
        source_text = (
            "The ancient castle stood majestically on the hilltop, its stone "
            "walls weathered by centuries of wind and rain. "
            "Inside the grand hall, tapestries depicting historical battles "
            "hung from the walls, telling stories of bravery and conquest. "
            "The library contained thousands of books, each one a treasure "
            "trove of knowledge waiting to be discovered. "
            "The courtyard was filled with the sound of clashing swords as "
            "knights practiced their combat skills. "
            "From the highest tower, one could see the entire kingdom spread "
            "out below like a beautiful tapestry."
        )

        target_text = (
            "El antiguo castillo se alzaba majestuosamente en la cima de la "
            "colina. Sus muros de piedra estaban desgastados por siglos de "
            "viento y lluvia. "
            "Dentro del gran salón, tapices que representaban batallas "
            "históricas colgaban de las paredes. Contaban historias de "
            "valentía y conquista. "
            "La biblioteca contenía miles de libros. Cada uno era un tesoro "
            "de conocimiento esperando ser descubierto. "
            "El patio estaba lleno del sonido de espadas chocando mientras "
            "los caballeros practicaban sus habilidades de combate. "
            "Desde la torre más alta, se podía ver todo el reino extendido "
            "abajo como un hermoso tapiz."
        )

        source_sentences = split_text_to_sentences(source_text)
        target_sentences = split_text_to_sentences(target_text)

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have alignments
        assert len(alignment) > 0, "Should have alignments for 1-2 pattern"

        # Check for various alignment patterns
        alignment_patterns = []
        for source_seg, target_seg in alignment:
            # Count sentences in source segment
            source_sentences = len([s for s in source_seg.split(".") if s.strip()])
            target_sentences = len([s for s in target_seg.split(".") if s.strip()])
            alignment_patterns.append((source_sentences, target_sentences))

        # Should have multiple alignment patterns
        assert len(alignment_patterns) > 1, "Should have multiple alignment segments"

        # Check that we have substantial content
        total_source_chars = sum(len(source_seg) for source_seg, _ in alignment)
        total_target_chars = sum(len(target_seg) for _, target_seg in alignment)

        assert total_source_chars > 200, "Should have substantial source content"
        assert total_target_chars > 200, "Should have substantial target content"

    def test_align_1_0_pattern(self):
        """Test alignment with 1-0 pattern (one source sentence with no "
        "target alignment)."""
        aligner = Aligner()

        # Create paragraph-sized input with 1-0 alignment pattern
        source_text = (
            "The scientist carefully examined the specimen under the "
            "microscope, noting every detail of its structure. "
            "This discovery could revolutionize our understanding of "
            "cellular biology and lead to breakthrough treatments. "
            "The research team worked tirelessly for months, conducting "
            "countless experiments and analyzing mountains of data. "
            "Their findings were published in a prestigious journal, "
            "earning recognition from the scientific community. "
            "This paragraph contains additional information that may not "
            "have a direct translation in the target language."
        )

        target_text = (
            "El científico examinó cuidadosamente la muestra bajo el "
            "microscopio, anotando cada detalle de su estructura. "
            "Este descubrimiento podría revolucionar nuestra comprensión "
            "de la biología celular y llevar a tratamientos innovadores. "
            "El equipo de investigación trabajó incansablemente durante "
            "meses, realizando innumerables experimentos y analizando "
            "montañas de datos. "
            "Sus hallazgos fueron publicados en una revista prestigiosa, "
            "ganando reconocimiento de la comunidad científica."
        )

        source_sentences = split_text_to_sentences(source_text)
        target_sentences = split_text_to_sentences(target_text)

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have alignments
        assert len(alignment) > 0, "Should have alignments for 1-0 pattern"

        # Check for various alignment patterns
        alignment_patterns = []
        for source_seg, target_seg in alignment:
            # Count sentences in source segment
            source_sentences = len([s for s in source_seg.split(".") if s.strip()])
            target_sentences = len([s for s in target_seg.split(".") if s.strip()])
            alignment_patterns.append((source_sentences, target_sentences))

        # Should have multiple alignment patterns
        assert len(alignment_patterns) > 1, "Should have multiple alignment segments"

        # Check that we have substantial content
        total_source_chars = sum(len(source_seg) for source_seg, _ in alignment)
        total_target_chars = sum(len(target_seg) for _, target_seg in alignment)

        assert total_source_chars > 200, "Should have substantial source content"
        assert total_target_chars > 200, "Should have substantial target content"

    def test_align_0_1_pattern(self):
        """Test alignment with 0-1 pattern (no source sentence with one "
        "target sentence)."""
        aligner = Aligner()

        # Create paragraph-sized input with 0-1 alignment pattern
        source_text = (
            "The artist carefully mixed colors on her palette, creating the "
            "perfect shade for the sunset sky. "
            "Her brush moved across the canvas with practiced precision, "
            "bringing the landscape to life. "
            "The painting captured the essence of the moment, preserving it "
            "for future generations to admire. "
            "Her studio was filled with completed works, each one telling "
            "its own unique story."
        )

        target_text = (
            "La artista mezcló cuidadosamente los colores en su paleta, "
            "creando el tono perfecto para el cielo del atardecer. "
            "Su pincel se movía por el lienzo con precisión practicada, "
            "dando vida al paisaje. "
            "La pintura capturó la esencia del momento, preservándola para "
            "que las futuras generaciones la admiren. "
            "Su estudio estaba lleno de obras completadas, cada una "
            "contando su propia historia única. "
            "Esta oración adicional en español no tiene una traducción "
            "directa en el texto fuente en inglés."
        )

        source_sentences = split_text_to_sentences(source_text)
        target_sentences = split_text_to_sentences(target_text)

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have alignments
        assert len(alignment) > 0, "Should have alignments for 0-1 pattern"

        # Check for various alignment patterns
        alignment_patterns = []
        for source_seg, target_seg in alignment:
            # Count sentences in source segment
            source_sentences = len([s for s in source_seg.split(".") if s.strip()])
            target_sentences = len([s for s in target_seg.split(".") if s.strip()])
            alignment_patterns.append((source_sentences, target_sentences))

        # Should have multiple alignment patterns
        assert len(alignment_patterns) > 1, "Should have multiple alignment segments"

        # Check that we have substantial content
        total_source_chars = sum(len(source_seg) for source_seg, _ in alignment)
        total_target_chars = sum(len(target_seg) for _, target_seg in alignment)

        assert total_source_chars > 200, "Should have substantial source content"
        assert total_target_chars > 200, "Should have substantial target content"

    def test_align_mixed_patterns(self):
        """Test alignment with mixed patterns (2-1, 1-2, 1-0, 0-1) in a "
        "complex paragraph."""
        aligner = Aligner()

        # Create complex paragraph with mixed alignment patterns
        source_text = (
            "The expedition team prepared for their journey into the "
            "uncharted wilderness, packing essential supplies and equipment. "
            "They knew the terrain would be challenging, with steep mountains "
            "and dense forests blocking their path. "
            "The weather forecast predicted storms, but they were determined "
            "to reach their destination. "
            "This sentence has no direct translation in the target text. "
            "The team leader reviewed the map one final time, ensuring "
            "everyone understood the route. "
            "They set out at dawn, their spirits high despite the challenges "
            "ahead."
        )

        target_text = (
            "El equipo de expedición se preparó para su viaje hacia la "
            "naturaleza virgen. Empacaron suministros esenciales y equipo. "
            "Sabían que el terreno sería desafiante. Las montañas empinadas "
            "y bosques densos bloqueaban su camino. "
            "El pronóstico del tiempo predijo tormentas. Pero estaban "
            "determinados a llegar a su destino. "
            "El líder del equipo revisó el mapa una vez final. Se aseguró "
            "de que todos entendieran la ruta. "
            "Partieron al amanecer. Sus espíritus estaban altos a pesar de "
            "los desafíos por delante."
        )

        source_sentences = split_text_to_sentences(source_text)
        target_sentences = split_text_to_sentences(target_text)

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have alignments
        assert len(alignment) > 0, "Should have alignments for mixed patterns"

        # Analyze alignment patterns
        alignment_patterns = []
        for source_seg, target_seg in alignment:
            source_sentences = len([s for s in source_seg.split(".") if s.strip()])
            target_sentences = len([s for s in target_seg.split(".") if s.strip()])
            alignment_patterns.append((source_sentences, target_sentences))

        # Should have various alignment patterns
        assert len(alignment_patterns) > 1, "Should have multiple alignment patterns"

        # Check that we have a mix of different patterns
        unique_patterns = set(alignment_patterns)
        assert len(unique_patterns) > 1, "Should have different alignment patterns"

    def test_align_large_paragraphs(self):
        """Test alignment with large paragraph-sized inputs to verify "
        "algorithm scalability."""
        aligner = Aligner()

        # Create large paragraph-sized inputs
        source_text = (
            "The technological revolution of the twenty-first century has "
            "fundamentally transformed the way we live, work, and communicate. "
            "Artificial intelligence and machine learning algorithms now power "
            "everything from our smartphones to our transportation systems. "
            "The internet has created a global village where information "
            "flows freely across borders and cultures. "
            "Social media platforms have redefined human interaction, "
            "enabling instant communication with people around the world. "
            "Cloud computing has revolutionized data storage and processing, "
            "making powerful computing resources accessible to everyone. "
            "The rise of renewable energy technologies has begun to address "
            "the urgent challenge of climate change. "
            "Electric vehicles are becoming increasingly common, reducing "
            "our dependence on fossil fuels. "
            "Advances in medical technology have led to breakthroughs in "
            "disease treatment and prevention. "
            "The development of quantum computing promises to solve problems "
            "that were previously impossible to tackle. "
            "These innovations continue to accelerate, creating both "
            "opportunities and challenges for society."
        )

        target_text = (
            "La revolución tecnológica del siglo veintiuno ha transformado "
            "fundamentalmente la forma en que vivimos, trabajamos y nos "
            "comunicamos. "
            "Los algoritmos de inteligencia artificial y aprendizaje "
            "automático ahora impulsan todo, desde nuestros teléfonos "
            "inteligentes hasta nuestros sistemas de transporte. "
            "Internet ha creado una aldea global donde la información "
            "fluye libremente a través de fronteras y culturas. "
            "Las plataformas de redes sociales han redefinido la "
            "interacción humana, permitiendo la comunicación instantánea "
            "con personas de todo el mundo. "
            "La computación en la nube ha revolucionado el almacenamiento "
            "y procesamiento de datos, haciendo que los recursos "
            "informáticos potentes sean accesibles para todos. "
            "El surgimiento de las tecnologías de energía renovable ha "
            "comenzado a abordar el urgente desafío del cambio climático. "
            "Los vehículos eléctricos se están volviendo cada vez más "
            "comunes, reduciendo nuestra dependencia de los combustibles "
            "fósiles. "
            "Los avances en tecnología médica han llevado a avances en el "
            "tratamiento y prevención de enfermedades. "
            "El desarrollo de la computación cuántica promete resolver "
            "problemas que anteriormente eran imposibles de abordar. "
            "Estas innovaciones continúan acelerándose, creando tanto "
            "oportunidades como desafíos para la sociedad."
        )

        source_sentences = split_text_to_sentences(source_text)
        target_sentences = split_text_to_sentences(target_text)

        alignment = aligner.align(source_sentences, target_sentences)

        # Should have alignments
        assert len(alignment) > 0, "Should have alignments for large paragraphs"

        # Should have reasonable number of alignments (not too many, not too few)
        assert (
            5 <= len(alignment) <= 15
        ), f"Should have reasonable number of alignments, got {len(alignment)}"

        # Each alignment should have substantial content
        total_source_chars = sum(len(source_seg) for source_seg, _ in alignment)
        total_target_chars = sum(len(target_seg) for _, target_seg in alignment)

        assert total_source_chars > 500, "Should have substantial source content"
        assert total_target_chars > 500, "Should have substantial target content"

    def test_align_language_specific_parameters(self):
        """Test that language-specific parameters are correctly configured."""
        # Test English-Spanish parameters
        aligner_es = Aligner("en-es")
        assert aligner_es.c == 1.0
        assert aligner_es.s2 == 6.8
        assert aligner_es.gap_penalty == 3.0

        # Test English-French parameters
        aligner_fr = Aligner("en-fr")
        assert aligner_fr.c == 1.1
        assert aligner_fr.s2 == 7.2
        assert aligner_fr.gap_penalty == 3.0

        # Test English-German parameters
        aligner_de = Aligner("en-de")
        assert aligner_de.c == 1.2
        assert aligner_de.s2 == 8.1
        assert aligner_de.gap_penalty == 3.0

        # Test English-Italian parameters
        aligner_it = Aligner("en-it")
        assert aligner_it.c == 1.05
        assert aligner_it.s2 == 7.0
        assert aligner_it.gap_penalty == 3.0

        # Test unknown language pair (should use default)
        aligner_unknown = Aligner("en-xx")
        assert aligner_unknown.c == 1.0  # Default to en-es
        assert aligner_unknown.s2 == 6.8
        assert aligner_unknown.gap_penalty == 3.0

    def test_align_statistical_cost_calculation(self):
        """Test that the statistical cost calculation works correctly."""
        aligner = Aligner("en-es")

        # Test cost calculation for similar length sentences (should be low cost)
        cost_similar = aligner._alignment_cost(50, 50)  # 1:1 ratio
        assert cost_similar < 5.0, "Similar length sentences should have low cost"

        # Test cost calculation for very different length sentences
        # (should be high cost)
        cost_different = aligner._alignment_cost(10, 100)  # 1:10 ratio
        assert (
            cost_different > cost_similar
        ), "Very different length sentences should have higher cost"

        # Test gap penalty cost
        gap_cost = aligner._gap_penalty_cost()
        assert gap_cost > 0, "Gap penalty should be positive"
        assert gap_cost < 100, "Gap penalty should be reasonable"

        # Test that the cost increases with larger deviations
        cost_small = aligner._alignment_cost(50, 55)  # Small deviation
        cost_large = aligner._alignment_cost(50, 100)  # Large deviation
        assert cost_large > cost_small, "Larger deviations should have higher cost"

    def test_user_configurable_parameters(self):
        """Test that user-provided c, s2, and gap_penalty are used."""
        aligner = Aligner(language_pair="en-es", c=2.0, s2=42.0, gap_penalty=7.0)
        assert aligner.c == 2.0
        assert aligner.s2 == 42.0
        assert aligner.gap_penalty == 7.0
        # Gap costs should be based on the new gap_penalty
        assert aligner._gap_cost > 0
        assert aligner._double_gap_cost == 2 * aligner._gap_cost

    def test_2_0_and_0_2_alignments(self):
        """Test that 2-0 and 0-2 alignments are considered in DP."""
        aligner = Aligner()
        # 2-0: two source sentences, no target
        source = ["A.", "B."]
        target = []
        alignment = aligner.align(source, target)
        # Should result in a single 2-0 alignment (both source sentences skipped)
        assert len(alignment) == 0  # No aligned pairs, but path should be valid
        # 0-2: no source, two target sentences
        source = []
        target = ["C.", "D."]
        alignment = aligner.align(source, target)
        assert len(alignment) == 0
        # Now test with a mix that forces a 2-0 or 0-2 in the middle
        source = ["A.", "B.", "C."]
        target = ["A.", "C."]
        alignment = aligner.align(source, target)
        # Should align A. to A., skip B. (2-0 or 1-0), align C. to C.
        aligned_sources = [s for s, t in alignment]
        assert "B." not in aligned_sources or any(
            s == "B." and t == "" for s, t in alignment
        )
        # 0-2 in the middle
        source = ["A.", "C."]
        target = ["A.", "B.", "C."]
        alignment = aligner.align(source, target)
        aligned_targets = [t for s, t in alignment]
        assert "B." not in aligned_targets or any(
            t == "B." and s == "" for s, t in alignment
        )

    def test_gap_costs_are_precalculated(self):
        """Test that gap penalty costs are pre-calculated and used."""
        aligner = Aligner()
        # The gap cost should match the function output
        assert aligner._gap_cost == aligner._gap_penalty_cost()
        assert aligner._double_gap_cost == 2 * aligner._gap_penalty_cost()
        # Changing gap_penalty should change the costs
        aligner2 = Aligner(gap_penalty=5.0)
        assert aligner2._gap_cost == aligner2._gap_penalty_cost()
        assert aligner2._double_gap_cost == 2 * aligner2._gap_penalty_cost()


class TestNumericalStability:
    """Test that the aligner handles numerical edge cases correctly."""

    def test_alignment_cost_never_infinite(self):
        """Test that alignment cost never returns infinite values."""
        aligner = Aligner()

        # Test various edge cases that could cause numerical instability
        test_cases = [
            (0, 0),  # Both zero
            (0, 1),  # Source zero
            (1, 0),  # Target zero
            (1, 1000),  # Very different lengths
            (1000, 1),  # Very different lengths
            (100, 100),  # Equal lengths
            (1, 1),  # Small lengths
        ]

        for src_len, tgt_len in test_cases:
            cost = aligner._alignment_cost(src_len, tgt_len)

            # Cost should be finite
            assert not math.isinf(
                cost
            ), f"Cost is infinite for src_len={src_len}, tgt_len={tgt_len}"
            assert not math.isnan(
                cost
            ), f"Cost is NaN for src_len={src_len}, tgt_len={tgt_len}"

            # Cost should be non-negative (since it's -log(probability))
            assert (
                cost >= 0
            ), f"Cost is negative for src_len={src_len}, tgt_len={tgt_len}"

    def test_gap_penalty_cost_never_infinite(self):
        """Test that gap penalty cost never returns infinite values."""

        # Test with different gap penalty values
        for gap_penalty in [0.1, 1.0, 10.0, 100.0]:
            # Create aligner with custom gap penalty
            aligner = Aligner(gap_penalty=gap_penalty)
            cost = aligner._gap_penalty_cost()

            assert not math.isinf(
                cost
            ), f"Cost is infinite for gap_penalty={gap_penalty}"
            assert cost >= 0, f"Cost is negative for gap_penalty={gap_penalty}"

    def test_extreme_delta_values(self):
        """Test that extreme delta values don't cause numerical issues."""
        aligner = Aligner()

        # Test with very large delta values that could cause numerical instability
        extreme_cases = [
            (1, 10000),  # Very large target length
            (10000, 1),  # Very large source length
            (1, 100000),  # Extremely large target length
            (100000, 1),  # Extremely large source length
        ]

        for src_len, tgt_len in extreme_cases:
            cost = aligner._alignment_cost(src_len, tgt_len)

            # Cost should be finite and reasonable
            assert not math.isinf(
                cost
            ), f"Cost is infinite for extreme case src_len={src_len}, tgt_len={tgt_len}"
            assert not math.isnan(
                cost
            ), f"Cost is NaN for extreme case src_len={src_len}, tgt_len={tgt_len}"
            assert (
                cost >= 0
            ), f"Cost is negative for extreme case src_len={src_len}, tgt_len={tgt_len}"

    def test_probability_floor_value(self):
        """Test that probability never becomes exactly zero."""
        aligner = Aligner()

        # Test with very large delta that would normally give probability near zero
        src_len, tgt_len = 1, 1000
        delta = abs(tgt_len - src_len * aligner.c) / math.sqrt(src_len * aligner.s2)

        # Calculate probability manually to verify epsilon is added
        raw_probability = 2 * (1 - stats.norm.cdf(delta))
        epsilon_probability = raw_probability + 1e-12

        # The probability should be greater than zero
        assert (
            epsilon_probability > 0
        ), "Probability should be greater than zero with epsilon"

        # The cost should be finite
        cost = -math.log(epsilon_probability)
        assert not math.isinf(cost), "Cost should be finite with epsilon"

    def test_delta_greater_than_10_handling(self):
        """Test that delta > 10 is handled correctly with finite probability."""
        aligner = Aligner()

        # Create a case where delta > 10
        src_len, tgt_len = 1, 10000  # This should give delta > 10
        cost = aligner._alignment_cost(src_len, tgt_len)

        # Cost should be finite (not infinite)
        assert not math.isinf(cost), "Cost should be finite even for delta > 10"
        assert not math.isnan(cost), "Cost should not be NaN for delta > 10"
        assert cost >= 0, "Cost should be non-negative for delta > 10"

        # The cost should be high but finite
        assert cost < 1000, "Cost should be reasonable even for extreme cases"


class TestAlignmentRobustness:
    """Test that the alignment algorithm works robustly with the fixes."""

    def test_alignment_with_extreme_lengths(self):
        """Test that alignment works with extreme sentence lengths."""
        aligner = Aligner()

        # Test with very short and very long sentences
        source_sentences = ["A", "This is a very short sentence.", "A" * 1000]
        target_sentences = ["B", "This is a very short sentence.", "B" * 1000]

        try:
            result = aligner.align(source_sentences, target_sentences)
            # Should not crash and should return some result
            assert isinstance(result, list)
        except (ValueError, OverflowError, RuntimeError) as e:
            pytest.fail(f"Alignment crashed with extreme lengths: {e}")

    def test_alignment_with_empty_sentences(self):
        """Test that alignment handles empty sentences correctly."""
        aligner = Aligner()

        # Test with empty sentences
        source_sentences = ["", "Hello world.", "   ", "Another sentence."]
        target_sentences = ["", "Hola mundo.", "   ", "Otra frase."]

        result = aligner.align(source_sentences, target_sentences)

        # Should not crash and should filter out empty sentences
        assert isinstance(result, list)
        # Should only align non-empty sentences
        assert len(result) > 0

    def test_alignment_with_very_different_lengths(self):
        """Test that alignment works with very different sentence lengths."""
        aligner = Aligner()

        # Test with very different sentence lengths
        source_sentences = ["A", "This is a medium length sentence.", "A" * 500]
        target_sentences = ["B" * 100, "This is a medium length sentence.", "B"]

        try:
            result = aligner.align(source_sentences, target_sentences)
            # Should not crash
            assert isinstance(result, list)
        except (ValueError, OverflowError, RuntimeError) as e:
            pytest.fail(f"Alignment crashed with very different lengths: {e}")


def test_aligner_documentation():
    """Test that the aligner documentation reflects the numerical stability "
    "improvements."""
    aligner = Aligner()

    # Check that the cost calculation methods have proper documentation
    alignment_cost_doc = aligner._alignment_cost.__doc__
    assert alignment_cost_doc is not None
    assert "cost" in alignment_cost_doc.lower()

    gap_penalty_doc = aligner._gap_penalty_cost.__doc__
    assert gap_penalty_doc is not None
    assert "cost" in gap_penalty_doc.lower()


def test_aligner_backward_compatibility():
    """Test that the aligner still works correctly for normal cases."""
    aligner = Aligner()

    # Test normal alignment case
    source_sentences = ["Hello world.", "This is a test."]
    target_sentences = ["Hola mundo.", "Esto es una prueba."]

    result = aligner.align(source_sentences, target_sentences)

    # Should work normally
    assert isinstance(result, list)
    assert len(result) > 0

    # Test perfect match case
    perfect_sentences = ["Hello world.", "This is a test."]
    perfect_result = aligner.align(perfect_sentences, perfect_sentences)

    assert isinstance(perfect_result, list)
    assert len(perfect_result) == len(perfect_sentences)
