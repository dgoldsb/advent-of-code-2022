package aoc.structures;

import java.math.BigInteger;
import java.util.LinkedList;
import java.util.List;

public class RingBuffer<T> {
    private final LinkedList<T> items;
    private Integer pointer;

    public RingBuffer(List<T> list) {
        this.pointer = 0;
        this.items = new LinkedList<>();
        this.items.addAll(list);
    }

    public void rotate(int offset) {
        this.pointer += offset;
        this.pointer = this.normalize(this.pointer, this.items.size());
    }

    public void rotate(BigInteger offset) {
        BigInteger pointer = offset.add(new BigInteger(this.pointer.toString()));
        this.pointer = this.normalize(pointer, this.items.size());
    }

    public T peek() {
        return this.items.get(this.pointer);
    }

    public T removeLeft() {
        T value = this.items.remove(this.pointer.intValue());
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

    public int normalize(BigInteger index, int size) {
        return Integer.parseInt(index.mod(new BigInteger(Integer.toString(size))).toString());
    }

    private int normalize(Integer index, int size) {
        return this.normalize(new BigInteger(index.toString()), size);
    }

    public void putFirst(T identifier) {
        this.pointer = this.indexOf(identifier);
    }

    public List<T> toList() {
        this.rotate(-this.pointer);
        return this.items.stream().toList();
    }
}
