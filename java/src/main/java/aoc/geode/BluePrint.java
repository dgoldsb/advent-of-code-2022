package aoc.geode;

import java.util.ArrayDeque;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class BluePrint {
    int identifier;
    MineralCollection oreCost;
    MineralCollection clayCost;
    MineralCollection obsidianCost;
    MineralCollection geodeCost;

    public BluePrint(String line) {
        Pattern blueprintPattern = Pattern.compile("Blueprint (\\d+)\\D+(\\d+)\\D+(\\d+)\\D+(\\d+)\\D+(\\d+)\\D+(\\d+)\\D+(\\d+)\\D+\\.");
        Matcher matcher = blueprintPattern.matcher(line);
        if (matcher.find()) {
            this.identifier = Integer.parseInt(matcher.group(1));
            this.oreCost = new MineralCollection(Integer.parseInt(matcher.group(2)), 0, 0, 0);
            this.clayCost = new MineralCollection(Integer.parseInt(matcher.group(3)), 0, 0, 0);
            this.obsidianCost = new MineralCollection(Integer.parseInt(matcher.group(4)), Integer.parseInt(matcher.group(5)), 0, 0);
            this.geodeCost = new MineralCollection(Integer.parseInt(matcher.group(6)), 0, Integer.parseInt(matcher.group(7)), 0);
        } else {
            throw new RuntimeException("Invalid input '%s'".formatted(line));
        }
    }

    private int crackGeodes(int totalRunTime) {
        int best = 0;
        ArrayDeque<GeodeCollectionState> stack = new ArrayDeque<>();

        // Seed with two starting states.
        stack.add(new GeodeCollectionState(MineralType.ORE, totalRunTime));
        stack.add(new GeodeCollectionState(MineralType.CLAY, totalRunTime));

        // Set the maximum costs.
        int maxOreCost = Math.max(Math.max(this.oreCost.ore, this.clayCost.ore), Math.max(this.obsidianCost.ore, this.geodeCost.ore));
        int maxClayCost = Math.max(Math.max(this.oreCost.clay, this.clayCost.clay), Math.max(this.obsidianCost.clay, this.geodeCost.clay));
        int maxObsidianCost = Math.max(Math.max(this.oreCost.ore, this.clayCost.obsidian), Math.max(this.obsidianCost.obsidian, this.geodeCost.obsidian));

        while (!stack.isEmpty()) {
            GeodeCollectionState state = stack.remove();
            best = Math.max(best, state.collectedMinerals.geode);

            MineralCollection minerals = state.collectedMinerals;
            RobotCollection robots = state.accumulatedRobots;

            if (state.currentTime == state.totalRunTime || state.shouldPrune(best, maxOreCost, maxClayCost, maxObsidianCost)) {
                continue;
            }

            // Can I order a next robot?
            boolean building;
            MineralCollection price = switch (state.nextType) {
                case ORE -> this.oreCost;
                case CLAY -> this.clayCost;
                case OBSIDIAN -> this.obsidianCost;
                case GEODE -> this.geodeCost;
            };
            if (state.collectedMinerals.canAfford(price)) {
                building = true;
                minerals = state.collectedMinerals.subtract(price);
            } else {
                building = false;
                minerals = state.collectedMinerals;
            }

            // Mine!
            minerals = minerals.add(state.accumulatedRobots.produce());

            // Build, if any.
            if (building) {
                robots = switch (state.nextType) {
                    case ORE -> robots.add(new RobotCollection(1, 0, 0, 0));
                    case CLAY -> robots.add(new RobotCollection(0, 1, 0, 0));
                    case OBSIDIAN -> robots.add(new RobotCollection(0, 0, 1, 0));
                    case GEODE -> robots.add(new RobotCollection(0, 0, 0, 1));
                };
            } else {
                robots = state.accumulatedRobots;
            }

            GeodeCollectionState updatedState = new GeodeCollectionState(
                    state.nextType,
                    state.currentTime + 1,
                    state.totalRunTime,
                    minerals,
                    robots
            );
            if (building) {
                for (MineralType newType : updatedState.getPossibleNextTypes()) {
                    GeodeCollectionState newState = new GeodeCollectionState(
                            newType,
                            updatedState.currentTime,
                            updatedState.totalRunTime,
                            updatedState.collectedMinerals,
                            updatedState.accumulatedRobots
                    );
                    stack.addFirst(newState);
                }
            } else {
                stack.addFirst(updatedState);
            }
        }
        return best;
    }

    public int getGeodes(int totalRunTime) {
        return crackGeodes(totalRunTime);
    }

    public int getQuality(int totalRunTime) {
        return crackGeodes(totalRunTime) * this.identifier;
    }
}
