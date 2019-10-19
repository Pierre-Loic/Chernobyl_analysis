from chernobylapp import dataprocess
import pytest


#---------------------
# Test remove_n method
#---------------------
#=========
# Fixtures
#=========

#======
# Tests
#======


#----------------------
# Test check_srt method
#----------------------
#=========
# Fixtures
#=========
@pytest.fixture
def data_instance():
    return dataprocess.Data_import()

#======
# Tests
#======
def test_check_srt_text(data_instance):
    """ Test the detection of rst files """
    assert data_instance.check_srt("") is False
    assert data_instance.check_srt(" ") is False
    assert data_instance.check_srt(" afdsgfvfv46484-):;,") is False
    assert data_instance.check_srt(r"1\n00:00:42,710 --> 00:00:44,920") is True

def test_check_srt_wrongtype(data_instance):
    """ Test exception for wrong type of data """
    with pytest.raises(TypeError):
        assert data_instance.check_srt(None)
    with pytest.raises(TypeError):
        assert data_instance.check_srt(12)

    
        
