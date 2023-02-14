package aoc.geode;

import java.util.ArrayList;

public class GeodeCollectionState {
    MineralType nextType;
    int currentTime;
    int totalRunTime;
    MineralCollection collectedMinerals;
    RobotCollection accumulatedRobots;

    public GeodeCollectionState(MineralType nextType, int totalRunTime) {
        this.nextType = nextType;
        this.currentTime = 0;
        this.totalRunTime = totalRunTime;
        this.collectedMinerals = new MineralCollection();
        this.accumulatedRobots = new RobotCollection();
    }

    public GeodeCollectionState(MineralType nextType, int currentTime, int totalRunTime, MineralCollection collectedMinerals, RobotCollection accumulatedRobots) {
        this.nextType = nextType;
        this.currentTime = currentTime;
        this.totalRunTime = totalRunTime;
        this.collectedMinerals = collectedMinerals;
        this.accumulatedRobots = accumulatedRobots;
    }

    public ArrayList<MineralType> getPossibleNextTypes() {
        ArrayList<MineralType> possibleNextTypes = new ArrayList<>();
        possibleNextTypes.add(MineralType.ORE);
        possibleNextTypes.add(MineralType.CLAY);
        if (this.accumulatedRobots.clay > 0) {
            possibleNextTypes.add(MineralType.OBSIDIAN);
        }
        if (this.accumulatedRobots.obsidian > 0) {
            possibleNextTypes.add(MineralType.GEODE);
        }
        return possibleNextTypes;
    }

    private int rangeSum(int number) {
        return (number * (number + 1)) / 2;
    }

    public boolean shouldPrune(int best, int oreCost, int clayCost, int obsidianCost) {
        int remainingTime = this.totalRunTime - this.currentTime;

        if (
                (this.collectedMinerals.geode + (this.accumulatedRobots.geode * remainingTime) + rangeSum(remainingTime)) < best
        ) {
            return true;
        }

        return this.accumulatedRobots.ore > oreCost ||
                this.accumulatedRobots.clay > clayCost ||
                this.accumulatedRobots.obsidian > obsidianCost;
    }
}
