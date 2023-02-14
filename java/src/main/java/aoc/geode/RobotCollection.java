package aoc.geode;

public class RobotCollection {
    int ore;
    int clay;
    int obsidian;
    int geode;

    public RobotCollection() {
        this.ore = 1;
        this.clay = 0;
        this.obsidian = 0;
        this.geode = 0;
    }

    public RobotCollection(int ore, int clay, int obsidian, int geode) {
        this.ore = ore;
        this.clay = clay;
        this.obsidian = obsidian;
        this.geode = geode;
    }

    public RobotCollection add(RobotCollection other) {
        return new RobotCollection(
                this.ore + other.ore,
                this.clay + other.clay,
                this.obsidian + other.obsidian,
                this.geode + other.geode
        );
    }

    public MineralCollection produce() {
        return new MineralCollection(
                this.ore,
                this.clay,
                this.obsidian,
                this.geode
        );
    }

}
