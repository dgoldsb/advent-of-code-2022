package aoc.aoc2022;

import aoc.structures.RingBuffer;
import org.junit.Test;

import java.util.Optional;
import java.util.stream.Stream;

import static org.junit.Assert.assertEquals;


public class RingBufferTest {
    @Test
    public void testAppendLeft1() {
        // Given
        RingBuffer<Integer> buffer = new RingBuffer<>(Stream.of(1));

        // When
        buffer.appendLeft(2);

        // Then
        int currentHead = buffer.peek();
        assertEquals(1, currentHead);
    }
}
