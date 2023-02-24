package aoc.aoc2022;

import aoc.decrypt.MixableRingBuffer;
import org.junit.Test;

import java.math.BigInteger;
import java.util.List;
import java.util.stream.Stream;

import static org.junit.Assert.assertEquals;


public class MixableRingBufferTest {
    @Test
    public void testPutFirstOne() {
        // Given
        List<BigInteger> startSequence = Stream.of(1, 2, -3, 3, -2, 0, 4).map(integer -> new BigInteger(integer.toString())).toList();
        MixableRingBuffer buffer = new MixableRingBuffer(startSequence);

        // When
        buffer.putFirst(2);

        // Then
        BigInteger head = buffer.peekValue();
        assertEquals(new BigInteger("-3"), head);
    }

    @Test
    public void testMixLarge() {
        // Given
        List<BigInteger> startSequence = Stream.of(702, 2, -3, 3, -2, 0, 4).map(i -> new BigInteger(i.toString())).toList();
        List<BigInteger> expectedSequence1 = Stream.of(2, -3, 702, 3, -2, 0, 4).map(i -> new BigInteger(i.toString())).toList();
        MixableRingBuffer buffer = new MixableRingBuffer(startSequence);

        // When
        buffer.mix(0);

        // Then
        assertEquals(expectedSequence1, buffer.toValueList());
    }

    @Test
    public void testMixLargeNegative() {
        // Given
        List<BigInteger> startSequence = Stream.of(-702, 2, -3, 3, -2, 0, 4).map(i -> new BigInteger(i.toString())).toList();
        List<BigInteger> expectedSequence1 = Stream.of(2, -3, 3, -2, -702, 0, 4).map(i -> new BigInteger(i.toString())).toList();
        MixableRingBuffer buffer = new MixableRingBuffer(startSequence);

        // When
        buffer.mix(0);

        // Then
        assertEquals(expectedSequence1, buffer.toValueList());
    }

    @Test
    public void testMix() {
        // Given
        List<BigInteger> startSequence = Stream.of(1, 2, -3, 3, -2, 0, 4).map(i -> new BigInteger(i.toString())).toList();
        List<BigInteger> expectedSequence1 = Stream.of(2, 1, -3, 3, -2, 0, 4).map(i -> new BigInteger(i.toString())).toList();
        List<BigInteger> expectedSequence2 = Stream.of(1, -3, 2, 3, -2, 0, 4).map(i -> new BigInteger(i.toString())).toList();
        List<BigInteger> expectedSequence3 = Stream.of(1, 2, 3, -2, -3, 0, 4).map(i -> new BigInteger(i.toString())).toList();
        List<BigInteger> expectedSequence4 = Stream.of(1, 2, -2, -3, 0, 3, 4).map(i -> new BigInteger(i.toString())).toList();
        List<BigInteger> expectedSequence5 = Stream.of(-2, 1, 2, -3, 0, 3, 4).map(i -> new BigInteger(i.toString())).toList();
        List<BigInteger> expectedSequence6 = Stream.of(-2, 1, 2, -3, 0, 3, 4).map(i -> new BigInteger(i.toString())).toList();
        List<BigInteger> expectedSequence7 = Stream.of(-2, 1, 2, -3, 4, 0, 3).map(i -> new BigInteger(i.toString())).toList();

        MixableRingBuffer buffer = new MixableRingBuffer(startSequence);

        // When
        buffer.mix(0);

        // Then
        assertEquals(expectedSequence1, buffer.toValueList());

        // When
        buffer.mix(1);

        // Then
        assertEquals(expectedSequence2, buffer.toValueList());

        // When
        buffer.mix(2);

        // Then
        assertEquals(expectedSequence3, buffer.toValueList());

        // When
        buffer.mix(3);

        // Then
        assertEquals(expectedSequence4, buffer.toValueList());

        // When
        buffer.mix(4);

        // Then
        assertEquals(expectedSequence5, buffer.toValueList());

        // When
        buffer.mix(5);

        // Then
        assertEquals(expectedSequence6, buffer.toValueList());

        // When
        buffer.mix(6);

        // Then
        assertEquals(expectedSequence7, buffer.toValueList());
    }

    @Test
    public void testMixEdgeCase() {
        // Given
        List<BigInteger> startSequence = Stream.of(0, -1, -1, 1).map(i -> new BigInteger(i.toString())).toList();
        List<BigInteger> expectedSequence1 = Stream.of(0, -1, -1, 1).map(i -> new BigInteger(i.toString())).toList();
        List<BigInteger> expectedSequence2 = Stream.of(-1, 0, -1, 1).map(i -> new BigInteger(i.toString())).toList();
        List<BigInteger> expectedSequence3 = Stream.of(-1, -1, 0, 1).map(i -> new BigInteger(i.toString())).toList();
        List<BigInteger> expectedSequence4 = Stream.of(-1, 1, -1, 0).map(i -> new BigInteger(i.toString())).toList();

        MixableRingBuffer buffer = new MixableRingBuffer(startSequence);

        // When
        buffer.mix(0);

        // Then
        assertEquals(expectedSequence1, buffer.toValueList());

        // When
        buffer.mix(1);

        // Then
        assertEquals(expectedSequence2, buffer.toValueList());

        // When
        buffer.mix(2);

        // Then
        assertEquals(expectedSequence3, buffer.toValueList());

        // When
        buffer.mix(3);

        // Then
        assertEquals(expectedSequence4, buffer.toValueList());
    }
}
