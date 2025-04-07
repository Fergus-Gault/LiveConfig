from liveconfig.decorators import livefunction

@livefunction
def sample_function(a, b, c=0):
    return a * b + c

def test_livefunction_tracks_args_and_kwargs():
    # Call the function with positional and keyword arguments
    result = sample_function(2, 3, c=4)
    
    # Assert the result of the function
    assert result == 10, "Expected result is 10"
    
    # Assert tracked positional arguments
    assert sample_function.tracked_params["args"] == (2, 3), "Tracked args should be (2, 3)"
    
    # Assert tracked keyword arguments
    assert sample_function.tracked_params["kwargs"] == {"c": 4}, "Tracked kwargs should be {'c': 4}"
    
    # Assert tracked parameter values
    expected_tracked_values = {"arg0": 2, "arg1": 3, "c": 4}
    assert sample_function.tracked_params_values == expected_tracked_values, f"Tracked params values should be {expected_tracked_values}"

def test_livefunction_no_kwargs():
    # Call the function with only positional arguments
    result = sample_function(5, 6)
    
    # Assert the result of the function
    assert result == 30, "Expected result is 30"
    
    # Assert tracked positional arguments
    assert sample_function.tracked_params["args"] == (5, 6), "Tracked args should be (5, 6)"
    
    # Assert tracked keyword arguments
    assert sample_function.tracked_params["kwargs"] == {}, "Tracked kwargs should be empty"
    
    # Assert tracked parameter values
    expected_tracked_values = {"arg0": 5, "arg1": 6}
    assert sample_function.tracked_params_values == expected_tracked_values, f"Tracked params values should be {expected_tracked_values}"