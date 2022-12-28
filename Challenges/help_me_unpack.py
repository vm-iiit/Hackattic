# The internal representation of negative numbers (int/floats) are language dependent.
# https://stackoverflow.com/q/74939927/8272292
# Initially tried implementing custom logic but that didn't work out due to above. 
# Therefore, falling back to library functions for decoding the signed ints/floats
# "struct" library reference - https://docs.python.org/3/library/struct.html

import base64
import requests
import sys
import json
import struct

BYTES=8
LEFTMOST_BIT_SET = (1 << ((BYTES*4)-1))
SHORT_LEFTMOST_BIT_SET = (1 << ((BYTES*2)-1))

access_token="access_token="  #Insert your access code here
hackattic_challenges_url="https://hackattic.com/challenges/"
problem_name="help_me_unpack/"

problem_url = hackattic_challenges_url+problem_name+"problem?"+access_token
submission_url = hackattic_challenges_url+problem_name+"solve?"+access_token

def get_problem_json(key, problem_url):
    problem_object = requests.get(problem_url)
    problem_json = problem_object.json()
    return problem_json[key]

def solve(key_having_problem_object):
    generic_problem_obj = get_problem_json(key_having_problem_object, problem_url)
    solution = solve_particular_problem(generic_problem_obj)
    submit_ans(solution)

def submit_ans(answer):
    print("sending "+json.dumps(answer)+" as the answer")
    ans_dict = answer
    response = requests.post(submission_url, json.dumps(ans_dict))
    print("submission response code "+str(response.status_code))
    print("submission reply - "+str(response.text))

def combine_bytes_to_int_or_float_big_endian(bytes_list):
    final_value = 0
    for i in range(len(bytes_list)):
        final_value += (bytes_list[i] << (BYTES * (len(bytes_list)-i-1)))
    return final_value

def combine_bytes_to_int_or_float_little_endian(bytes_list):
    final_value = 0
    for i in range(len(bytes_list)):
        final_value += (bytes_list[i] << (BYTES * (i)))
    return final_value


def signed_int(bytes_list):
    # integer_value = combine_bytes_to_int_or_float_little_endian(bytes_list)
    # sign = -1 if (integer_value & LEFTMOST_BIT_SET) else +1
    # integer_value = sign * (integer_value & (~LEFTMOST_BIT_SET) )
    # integer_value = (~integer_value) + 1
    final_val = struct.unpack('i', bytes (bytes_list))[0]
    return final_val

def unsigned_int(bytes_list):
    integer_value = combine_bytes_to_int_or_float_little_endian(bytes_list)
    # sign = -1 if (integer_value & (1 << (BYTES*4))) else +1
    # integer_value = sign * (integer_value & (~(1 << BYTES*4)))
    return integer_value

def short(bytes_list):
    # integer_value = combine_bytes_to_int_or_float_little_endian(bytes_list)
    # print("*-*-*-*")
    # print(struct.unpack('i', bytes (bytes_list)))
    # print("-*-*-*-*")
    # sign = -1 if (integer_value & SHORT_LEFTMOST_BIT_SET) else +1
    # short_abs_value = integer_value & (~SHORT_LEFTMOST_BIT_SET)
    # # integer_value = (~integer_value)
    # final_val = ((sign*short_abs_value) & 65535) 
    final_val = struct.unpack('h', bytes (bytes_list))[0]
    return final_val

def float(bytes_list):
    # value = combine_bytes_to_int_or_float_little_endian(bytes_list)
    # sign = -1 if (value & LEFTMOST_BIT_SET) else +1
    # exponent = ((value & ((255 << (BYTES*3)) >> 1)) >> 23)
    # mantissa = (value & (~(511 << (BYTES*4))))
    # float_value = None
    # # print("mantissa "+str(mantissa))
    # # print("exponent "+str(exponent))
    # if mantissa == 0 and exponent == 0:
    #     float_value = 0
    # elif exponent == 0 and mantissa:
    #     float_value = sign*(0+(0.1*mantissa))*pow(2,exponent-127)
    # else:
    #     float_value = sign*(1+(0.1*mantissa))*pow(2,exponent-127)
    final_val = struct.unpack('f', bytes (bytes_list))[0]
    return final_val

def double(bytes_list):
    # value = combine_bytes_to_int_or_float_little_endian(bytes_list)
    # sign = -1 if (value & LEFTMOST_BIT_SET) else +1
    # exponent = ((value & ((255 << (BYTES*7)) >> 1)) >> 52)
    # mantissa = (value & (~(511 << (BYTES*4))))
    # float_value = None
    # # print("mantissa "+str(mantissa))
    # # print("exponent "+str(exponent))
    # if mantissa == 0 and exponent == 0:
    #     float_value = 0
    # elif exponent == 0 and mantissa:
    #     float_value = sign*(0+(0.1*mantissa))*pow(2,exponent-1023)
    # else:
    #     float_value = sign*(1+(0.1*mantissa))*pow(2,exponent-1023)
    final_val = struct.unpack('d', bytes (bytes_list))[0]
    return final_val

def big_endian_double(bytes_list):
    # value = combine_bytes_to_int_or_float_big_endian(bytes_list)
    # sign = -1 if (value & ((1 << (BYTES*4)) >> 1)) else +1
    # exponent = ((value & ((255 << (BYTES*7)) >> 1)) >> 52)
    # mantissa = (value & (~(511 << (BYTES*4))))
    # float_value = None
    # # print("mantissa "+str(mantissa))
    # # print("exponent "+str(exponent))
    # if mantissa == 0 and exponent == 0:
    #     float_value = 0
    # elif exponent == 0 and mantissa:
    #     float_value = sign*(0+(0.1*mantissa))*pow(2,exponent-1023)
    # else:
    #     float_value = sign*(1+(0.1*mantissa))*pow(2,exponent-1023)
    final_val = struct.unpack('>d', bytes (bytes_list))[0]
    return final_val

def solve_particular_problem(input_problem_obj):
    base_64_encoded_obj = input_problem_obj
    base_64_decoded_obj = base64.b64decode(base_64_encoded_obj)
    bytes_list = [byte for byte in base_64_decoded_obj]
    print("bytes count "+str(len(bytes_list)))
    print(bytes_list)
    signed_int_value = signed_int(bytes_list[0:4])
    print("signed int "+str(signed_int_value))
    unsigned_int_value = unsigned_int(bytes_list[4:8]) 
    print("unsigned_int_value "+str(unsigned_int_value))
    short_value = short(bytes_list[8:10])
    print("short_value "+str(short_value))
    float_value = float(bytes_list[12:16])
    print("float_value "+str(float_value))
    double_value = double(bytes_list[16:24])
    print("double_value "+str(double_value))
    big_endian_double_value = big_endian_double(bytes_list[24:32])
    print("big_endian_double "+str(big_endian_double_value))

    ans_dict = {

        "int": signed_int_value,
        "uint": unsigned_int_value,
        "short": short_value,
        "float": float_value,
        "double": double_value,
        "big_endian_double": big_endian_double_value

    }
    
    return ans_dict

solve("bytes")
