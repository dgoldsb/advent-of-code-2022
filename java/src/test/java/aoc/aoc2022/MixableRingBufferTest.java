package aoc.aoc2022;

import aoc.decrypt.MixItem;
import aoc.decrypt.MixableRingBuffer;
import org.junit.Test;

import java.util.List;
import java.util.stream.IntStream;
import java.util.stream.Stream;

import static org.junit.Assert.assertEquals;


public class MixableRingBufferTest {
    @Test
    public void testMix() {
        // Given
        List<Integer> startSequence = Stream.of(1, 2, -3, 3, -2, 0, 4).toList();
        List<Integer> expectedSequence1 = Stream.of(2, 1, -3, 3, -2, 0, 4).toList();
        List<Integer> expectedSequence2 = Stream.of(1, -3, 2, 3, -2, 0, 4).toList();
        List<Integer> expectedSequence3 = Stream.of(1, 2, 3, -2, -3, 0, 4).toList();
        List<Integer> expectedSequence4 = Stream.of(1, 2, -2, -3, 0, 3, 4).toList();
        Stream<MixItem> mixItemStream = IntStream
                .range(0, startSequence.size())
                .mapToObj(i -> new MixItem(i, startSequence.get(i)));
        MixableRingBuffer buffer = new MixableRingBuffer(mixItemStream);

        // When
        buffer.mix(1);

        // Then
        assertEquals(expectedSequence1, buffer.toValueList());

        // When
        buffer.mix(2);

        // Then
        assertEquals(expectedSequence2, buffer.toValueList());

        // When
        buffer.mix(-3);

        // Then
        assertEquals(expectedSequence3, buffer.toValueList());

        // When
        buffer.mix(3);

        // Then
        assertEquals(expectedSequence4, buffer.toValueList());
    }
}
