package aoc.structures;

import java.math.BigInteger;
import java.util.LinkedList;
import java.util.List;

public class RingBuffer<T> {
    private final LinkedList<T> items;
    private int pointer;

    public RingBuffer(List<T> list) {
        this.pointer = 0;
        this.items = new LinkedList<>();
        this.items.addAll(list);
    }

    public void rotate(int offset) {
        this.pointer += offset;
        this.pointer = this.normalize(this.pointer);
    }

    public T peek() {
        return this.items.get(this.pointer);
    }

    public T removeLeft() {
        T value = this.items.remove(this.pointer);
        if (this.pointer > this.items.size()) {
            this.pointer = 0;
        }
        return value;
    }

    public void appendLeft(T value) {
        this.items.add(this.pointer, value);
        this.pointer += 1;
    }

    public int indexOf(T value) {
        return this.items.indexOf(value);
    }

    public int normalize(BigInteger index) {
        int size = this.items.size();
        int rotation = Integer.parseInt(index.mod(new BigInteger(Integer.toString(size))).toString());
        if (index.toString().charAt(0) == '-') {
            rotation -= 1;
        }
        return rotation;
    }

    private int normalize(Integer index) {
        return this.normalize(new BigInteger(index.toString()));
    }

    public void putFirst(T identifier) {
        this.pointer = this.indexOf(identifier);
    }

    public List<T> toList() {
        this.rotate(-this.pointer);
        return this.items.stream().toList();
    }
}
