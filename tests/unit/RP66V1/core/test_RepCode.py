"""
References:
RP66V1: http://w3.energistics.org/rp66/v1/rp66v1.html
Specifically Appendix B: http://w3.energistics.org/rp66/v1/rp66v1_appb.html

NOTE: Some test data is taken from RP66V2:
http://w3.energistics.org/rp66/v2/rp66v2.html
Specifically: http://w3.energistics.org/rp66/v2/rp66v2_sec2.html#11
"""
import pytest

from TotalDepth.RP66V1.core import RepCode
from TotalDepth.RP66V1.core.File import LogicalData


@pytest.mark.parametrize(
    'ld, expected',
    (
        # Examples from [RP66V1 Appendix B Section B.2]
        (LogicalData(b'\x43\x19\x00\x00'), 153.0),
        (LogicalData(b'\xc3\x19\x00\x00'), -153.0),
        # Example from RP66V2
        (LogicalData(b'\x00\x00\x00\x00'), 0.0),
    )
)
def test_FSINGL(ld, expected):
    result = RepCode.FSINGL(ld)
    assert result == expected
    assert ld.remain == 0


@pytest.mark.parametrize(
    'ld, expected',
    (
        # Examples from [RP66V1 Appendix B Section B.7 NOTE: These are only 4 byte examples, RP66V2 has better examples]
        (LogicalData(b'\x40\x63\x20\x00\x00\x00\x00\x00'), 153.0),
        (LogicalData(b'\xc0\x63\x20\x00\x00\x00\x00\x00'), -153.0),
        (LogicalData(b'\x00\x00\x00\x00\x00\x00\x00\x00'), 0.0),
    )
)
def test_FDOUBL(ld, expected):
    result = RepCode.FDOUBL(ld)
    assert result == expected
    assert ld.remain == 0


@pytest.mark.parametrize(
    'ld, expected',
    (
        (LogicalData(b'\x00'), 0),
        (LogicalData(b'\x59'), 89),
        (LogicalData(b'\x7f'), 127),
        (LogicalData(b'\x80'), -128),
        (LogicalData(b'\xa7'), -89),
        (LogicalData(b'\xff'), -1),
    )
)
def test_SSHORT(ld, expected):
    result = RepCode.SSHORT(ld)
    assert result == expected
    assert ld.remain == 0


@pytest.mark.parametrize(
    'ld, expected',
    (
        (LogicalData(b'\x00\x00'), 0),
        (LogicalData(b'\x00\x99'), 153),
        (LogicalData(b'\xff\x67'), -153),
    )
)
def test_SNORM(ld, expected):
    result = RepCode.SNORM(ld)
    assert result == expected
    assert ld.remain == 0


@pytest.mark.parametrize(
    'ld, expected',
    (
        (LogicalData(b'\x00\x00\x00\x00'), 0),
        (LogicalData(b'\x00\x00\x00\x99'), 153),
        (LogicalData(b'\xff\xff\xff\x67'), -153),
    )
)
def test_SLONG(ld, expected):
    result = RepCode.SLONG(ld)
    assert result == expected
    assert ld.remain == 0


@pytest.mark.parametrize(
    'ld, expected',
    (
        (LogicalData(b'\x00'), 0),
        (LogicalData(b'\xd9'), 217),  # RP66V2 example.
        (LogicalData(b'\xff'), 255),
    )
)
def test_USHORT(ld, expected):
    result = RepCode.USHORT(ld)
    assert result == expected
    assert ld.remain == 0


@pytest.mark.parametrize(
    'ld, expected',
    (
        (LogicalData(b'\x00\x00'), 0),
        (LogicalData(b'\x80\x99'), 32921),
        (LogicalData(b'\x00\x99'), 153),  # RP66V2 example.
    )
)
def test_UNORM(ld, expected):
    result = RepCode.UNORM(ld)
    assert result == expected
    assert ld.remain == 0


@pytest.mark.parametrize(
    'ld, expected',
    (
        (LogicalData(b'\x00\x00\x00\x00'), 0),
        (LogicalData(b'\x00\x00\x00\x99'), 153),
    )
)
def test_ULONG(ld, expected):
    result = RepCode.ULONG(ld)
    assert result == expected
    assert ld.remain == 0


@pytest.mark.parametrize(
    'ld, expected',
    (
        # One byte examples
        (LogicalData(b'\x00'), 0),
        (LogicalData(b'\x01'), 1),
        (LogicalData(b'\x7e'), 2**7 - 2),
        (LogicalData(b'\x7F'), 2**7 - 1),
        # Two byte examples
        (LogicalData(b'\x80\x80'), 2**7),
        (LogicalData(b'\x80\x81'), 2**7 + 1),
        (LogicalData(b'\xbf\xfe'), 2**14 - 2),
        (LogicalData(b'\xbf\xff'), 2**14 - 1),
        # Four byte examples
        (LogicalData(b'\xc0\x00\x40\x00'), 2**14),
        (LogicalData(b'\xc0\x00\x40\x01'), 2**14 + 1),
        (LogicalData(b'\xff\xff\xff\xfe'), 2**30 - 2),
        (LogicalData(b'\xff\xff\xff\xff'), 2**30 - 1),
    )
)
def test_UVARI(ld, expected):
    result = RepCode.UVARI(ld)
    assert result == expected
    assert ld.remain == 0


@pytest.mark.parametrize(
    'ld, expected',
    (
        (LogicalData(b'\x00'), b''),
        (LogicalData(b'\x03ABC'), b'ABC'),
        (LogicalData(b'\x05TYPE1'), b'TYPE1'),  # RP66V2 example.
    )
)
def test_IDENT(ld, expected):
    result = RepCode.IDENT(ld)
    assert result == expected
    assert ld.remain == 0


@pytest.mark.parametrize(
    'ld, expected',
    (
        (LogicalData(b'\x00'), b''),
        (LogicalData(b'\x03A\x0ab'), b'A\x0ab'),
        (LogicalData(b'\x05\x24 / \xa3'), b'\x24 / \xa3'),  # RP66V2 example.
    )
)
def test_ASCII(ld, expected):
    result = RepCode.ASCII(ld)
    assert result == expected
    assert ld.remain == 0


# TODO: Test DTIME out of range.
@pytest.mark.parametrize(
    'ld, expected',
    (
        (LogicalData(b'\x57\x14\x13\x15\x14\x0f\x02\x6c'), '1987-04-19 21:20:15.620'),
        # RP66V2 example from the printed standard. The website is in error as it uses all nulls.
        # http://w3.energistics.org/rp66/v2/rp66v2_sec2.html#11_4_2
        (LogicalData(b'\x00\x01\x01\x00\x00\x00\x00\x00'), '1900-01-01 00:00:00.000'),
    )
)
def test_DTIME(ld, expected):
    result = RepCode.DTIME(ld)
    assert str(result) == expected
    assert ld.remain == 0


@pytest.mark.parametrize(
    'ld, expected',
    (
        # One byte examples
        (LogicalData(b'\x00'), 0),
        (LogicalData(b'\x01'), 1),
        (LogicalData(b'\x7e'), 2**7 - 2),
        (LogicalData(b'\x7F'), 2**7 - 1),
        # Two byte examples
        (LogicalData(b'\x80\x80'), 2**7),
        (LogicalData(b'\x80\x81'), 2**7 + 1),
        (LogicalData(b'\xbf\xfe'), 2**14 - 2),
        (LogicalData(b'\xbf\xff'), 2**14 - 1),
        # Four byte examples
        (LogicalData(b'\xc0\x00\x40\x00'), 2**14),
        (LogicalData(b'\xc0\x00\x40\x01'), 2**14 + 1),
        (LogicalData(b'\xff\xff\xff\xfe'), 2**30 - 2),
        (LogicalData(b'\xff\xff\xff\xff'), 2**30 - 1),
    )
)
def test_ORIGIN(ld, expected):
    result = RepCode.ORIGIN(ld)
    assert result == expected
    assert ld.remain == 0


@pytest.mark.parametrize(
    'ld, expected',
    (
        (LogicalData(b'\x00' + b'\x01' + b'\x03ABC'), RepCode.ObjectName(0, 1, b'ABC')),
    )
)
def test_OBNAME(ld, expected):
    result = RepCode.OBNAME(ld)
    assert result == expected
    assert ld.remain == 0


@pytest.mark.parametrize(
    'ld, expected',
    (
        (
            LogicalData(
                b'\x0512345' + b'\x00' + b'\x01' + b'\x03ABC'
            ),
            RepCode.ObjectReference(
                RepCode.IDENT(LogicalData(b'\x0512345')),
                RepCode.ObjectName(0, 1, b'ABC'),
            ),
        ),
    )
)
def test_OBJREF(ld, expected):
    result = RepCode.OBJREF(ld)
    assert result == expected
    assert ld.remain == 0


@pytest.mark.parametrize(
    'ld, expected',
    (
        (LogicalData(b'\x00'), 0),
        (LogicalData(b'\x01'), 1),
    )
)
def test_STATUS(ld, expected):
    result = RepCode.STATUS(ld)
    assert result == expected
    assert ld.remain == 0


# TODO: Test: UNITS
# TODO: Test code_read()

