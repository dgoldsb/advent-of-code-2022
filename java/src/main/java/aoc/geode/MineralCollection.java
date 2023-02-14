package aoc.geode;

public class MineralCollection {
    int ore;
    int clay;
    int obsidian;
    int geode;

    public MineralCollection() {
        this.ore = 0;
        this.clay = 0;
        this.obsidian = 0;
        this.geode = 0;
    }

    public MineralCollection(int ore, int clay, int obsidian, int geode) {
        this.ore = ore;
        this.clay = clay;
        this.obsidian = obsidian;
        this.geode = geode;
    }

    public MineralCollection add(MineralCollection other) {
        return new MineralCollection(
                this.ore + other.ore,
                this.clay + other.clay,
                this.obsidian + other.obsidian,
                this.geode + other.geode
        );
    }

    public MineralCollection subtract(MineralCollection other) {
        return new MineralCollection(
                this.ore - other.ore,
                this.clay - other.clay,
                this.obsidian - other.obsidian,
                this.geode - other.geode
        );
    }

    public boolean canAfford(MineralCollection price) {
        return this.ore >= price.ore && this.clay >= price.clay && this.obsidian >= price.obsidian;
    }
}
