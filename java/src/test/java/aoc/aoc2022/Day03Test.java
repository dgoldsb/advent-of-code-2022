package aoc.aoc2022;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

import org.junit.Test;

import java.util.Optional;


public class Day03Test {
    @Test
    public void testFindA() {
        Day03 day = new Day03();
        Character result = day.findA("vJrwpWtwJgWrhcsFMMfFFhFp");
        assertEquals('p', result.charValue());
    }

    @Test
    public void testCharToIntLower() {
        Day03 day = new Day03();
        int result = day.charToInt('p');
        assertEquals(16, result);
    }

    @Test
    public void testCharToIntUpper() {
        Day03 day = new Day03();
        int result = day.charToInt('P');
        assertEquals(42, result);
    }
}
