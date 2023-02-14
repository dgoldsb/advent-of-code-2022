package aoc.aoc2022;

import aoc.geode.BluePrint;
import org.junit.Test;

import static org.junit.Assert.assertEquals;


public class Day19Test {
    @Test
    public void testBluePrint() {
        BluePrint bluePrint = new BluePrint("Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.");
        int result = bluePrint.getQuality(24);
        assertEquals(9, result);
    }
}
