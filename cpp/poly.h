#ifndef POLY_H
#define POLY_H

#include <algorithm>
#include <initializer_list>
#include <vector>

#include "monom.h"


class Poly {
    std::vector<Monom> mMonoms;

public:
    Poly() {};
    Poly(Monom& m) : mMonoms{m} {}
    Poly(std::initializer_list<Monom> monoms) : mMonoms(monoms) {
        std::sort(mMonoms.begin(), mMonoms.end());
    }
    Poly(std::vector<Monom>& monoms) : mMonoms(monoms) {
        std::sort(mMonoms.begin(), mMonoms.end());
    }
    Poly(const Poly& other) : mMonoms(other.mMonoms) {}
    Poly& operator=(const Poly& other) {
        if (this != &other) {
            mMonoms = other.mMonoms;
        }
        return *this;
    }
    Poly(const Poly&& other) noexcept : mMonoms(std::move(other.mMonoms)) {}
    const Poly& operator=(Poly&& other) noexcept {
        if (this != &other) {
            mMonoms = std::move(other.mMonoms);
        }
        return *this;
    }
    // ~Poly() {}

    bool isZero() const {
        return mMonoms.empty();
    }
    // TODO
    bool isOne() const {
        return mMonoms.size() == 1 && mMonoms[0].isOne();
        // return false
    }

    Monom lm() const {
        if (isZero())
            return Monom();
        // auto lm = std::max_element(mMonoms.begin(), mMonoms.end());
        // return *lm;
        return mMonoms.back();
    };

    bool operator==(const Poly&) const;
    Poly operator+(const Poly& b) const;
    Poly operator*(const Monom& b) const;
    Poly operator*(const Poly& b) const;

    friend std::ostream& operator<<(std::ostream& out, const Poly &a);
};

Poly spoly(const Poly&, const Poly&);
Poly normalform(const Poly&, const std::vector<Poly>&);

#endif // POLY_H
