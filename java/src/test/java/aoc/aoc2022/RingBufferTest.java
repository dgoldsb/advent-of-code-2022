package aoc.aoc2022;

import aoc.structures.RingBuffer;
import org.junit.Test;

import java.math.BigInteger;
import java.util.List;

import static org.junit.Assert.assertEquals;


public class RingBufferTest {
    @Test
    public void testNormalizePositiveModulo() {
        // Given
        RingBuffer<Integer> buffer = new RingBuffer<>(List.of(1, 2, 3, 4, 5, 6, 7));

        // When
        int result = buffer.normalize(new BigInteger("8"), 7);

        // Then
        assertEquals(2, result);
    }

    @Test
    public void testNormalizeNegativeNegativeModulo() {
        // Given
        RingBuffer<Integer> buffer = new RingBuffer<>(List.of(1, 2, 3, 4, 5, 6, 7));

        // When
        int result = buffer.normalize(new BigInteger("-1"), 7);

        // Then
        assertEquals(5, result);

        // When
        result = buffer.normalize(new BigInteger("-3"), 7);

        // Then
        assertEquals(3, result);

        // When
        result = buffer.normalize(new BigInteger("-6"), 7);

        // Then
        assertEquals(0, result);

        // When
        result = buffer.normalize(new BigInteger("-7"), 7);

        // Then
        assertEquals(5, result);

        // When
        result = buffer.normalize(new BigInteger("-16"), 7);

        // Then
        assertEquals(2, result);
    }

    @Test
    public void testAppendLeft() {
        // Given
        RingBuffer<Integer> buffer = new RingBuffer<>(List.of(1));

        // When
        buffer.appendLeft(2);

        // Then
        int currentHead = buffer.peek();
        assertEquals(1, currentHead);
    }
}
