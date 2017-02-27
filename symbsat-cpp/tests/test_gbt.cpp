#include "catch.hpp"

#include "monomt.h"
#include "polyt.h"
#include "zddt.h"
#include "gbt.h"

using namespace symbsat;

TEST_CASE("Buchberger 1 PolyZDD", "[buchberger-polyzdd]") {
    ZDD<Monoms::Monom32> x1(1), x2(2),
                         x3(4), x4(4), _1;
    _1.setOne();

    std::vector<ZDD<Monoms::Monom32>> F {
        x1 + x2 + x3 + x4,
        x1*x2 + x2*x3 + x1*x3 + x3*x4,
        x1*x2*x3 + x1*x2*x4 + x1*x3*x4 + x2*x3*x4,
        x1*x2*x3*x4 + _1
    };

    auto G = buchberger(F, 4);

    // for (auto& p: G)
        // std::cout << p << std::endl;

    REQUIRE(true);
}

TEST_CASE("Buchberger 1 PolyList", "[buchberger-polylist]") {
    Poly<Monoms::Monom32> x1(1), x2(2),
                          x3(4), x4(4), _1;
    _1.setOne();

    std::vector<Poly<Monoms::Monom32>> F {
        x1 + x2 + x3 + x4,
        x1*x2 + x2*x3 + x1*x3 + x3*x4,
        x1*x2*x3 + x1*x2*x4 + x1*x3*x4 + x2*x3*x4,
        x1*x2*x3*x4 + _1
    };

    auto G = buchberger(F, 4);

    // for (auto& p: G)
        // std::cout << p << std::endl;

    REQUIRE(true);
}

TEST_CASE("Buchberger 3 PolyZDD", "[buchberger3-polyzdd]") {
    ZDD<Monoms::Monom32> x1(1), x2(2), _1;
    _1.setOne();

    std::vector<ZDD<Monoms::Monom32>> F {
        x1*x2 + x1,
        x1*x2 + x2
    };

    auto G = buchberger(F, 2);

    REQUIRE(true);
}

TEST_CASE("Buchberger 3 PolyList", "[buchberger3-polylist]") {
    Poly<Monoms::Monom32> x1(1), x2(2), _1;
    _1.setOne();

    std::vector<Poly<Monoms::Monom32>> F {
        x1*x2 + x1,
        x1*x2 + x2
    };

    auto G = buchberger(F, 2);

    REQUIRE(true);
}

TEST_CASE("Buchberger 7 PolyZDD", "[buchberger7-polyzdd]") {
    ZDD<Monoms::Monom32> x1(1), x2(2), x3(3), _1;
    _1.setOne();

    std::vector<ZDD<Monoms::Monom32>> F {
        x1*x2*x3,
        x1*x2*x3 + x1*x2,
        x1*x2*x3 + x1*x3,
        x1*x2*x3 + x1*x2 + x1*x3 + x1,
        x1*x2*x3 + x2*x3,
        x1*x2*x3 + x1*x2 + x2*x3 + x2,
        x1*x2*x3 + x1*x3 + x2*x3 + x3,
        x1*x2*x3 + x1*x2 + x1*x3 + x1 + x2*x3 + x2 + x3 + _1
    };

    auto G = buchberger(F, 3);

    REQUIRE(true);
}

TEST_CASE("Buchberger 7 PolyList", "[buchberger7-polylist]") {
    Poly<Monoms::Monom32> x1(1), x2(2), x3(3), _1;
    _1.setOne();

    std::vector<Poly<Monoms::Monom32>> F {
        x1*x2*x3,
        x1*x2*x3 + x1*x2,
        x1*x2*x3 + x1*x3,
        x1*x2*x3 + x1*x2 + x1*x3 + x1,
        x1*x2*x3 + x2*x3,
        x1*x2*x3 + x1*x2 + x2*x3 + x2,
        x1*x2*x3 + x1*x3 + x2*x3 + x3,
        x1*x2*x3 + x1*x2 + x1*x3 + x1 + x2*x3 + x2 + x3 + _1
    };

    auto G = buchberger(F, 3);

    REQUIRE(true);
}
