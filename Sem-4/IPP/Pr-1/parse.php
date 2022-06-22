<?php

# project: IPP 1 ###
# author: xdudaj02 #
# file: parse.php ##

#### variables ####
$header = '.ippcode21'; # valid header
# valid instructions with mandatory arguments
# arguments: v - variable, s - constant or variable, t - type, l - label
$instructions = [
    "move" => "vs",
    "createframe" => "",
    "pushframe" => "",
    "popframe" => "",
    "defvar" => "v",
    "call" => "l",
    "return" => "",
    "pushs" => "s",
    "pops" => "v",
    "add" => "vss",
    "sub" => "vss",
    "mul" => "vss",
    "idiv" => "vss",
    "lt" => "vss",
    "gt" => "vss",
    "eq" => "vss",
    "and" => "vss",
    "or" => "vss",
    "not" => "vs",
    "int2char" => "vs",
    "stri2int" => "vss",
    "read" => "vt",
    "write" => "s",
    "concat" => "vss",
    "strlen" => "vs",
    "getchar" => "vss",
    "setchar" => "vss",
    "type" => "vs",
    "label" => "l",
    "jump" => "l",
    "jumpifeq" => "lss",
    "jumpifneq" => "lss",
    "exit" => "s",
    "dprint" => "s",
    "break" => "",
];

#### functions ####
# checks if parameter is a valid variable, returns 1 on success else 0
function is_variable($c) {
    return preg_match('/^[GLT]F@[a-zA-Z_\-$&%*!?][0-9a-zA-Z_\-$&%*!?]*$/', $c);
}
# checks if parameter is a valid constant, returns 1 on success else 0
function is_constant($c) {
    return preg_match('/^(int@[+\-]?\d+|bool@(true|false)|string@(?:[^\s#\\\\]|\\\\\d{3})*|nil@nil)$/', $c);
}
# checks if parameter is a valid label, returns 1 on success else 0
function is_label($c) {
    return preg_match('/^[a-zA-Z_\-\$&%*!?][0-9a-zA-Z_\-$&%*!?]*$/', $c);
}
# checks if parameter is a valid type, returns 1 on success else 0
function is_type($c) {
    return preg_match('/^(int|bool|string|nil)$/', $c);
}

#### argument parsing ####
# print help
if ($argc == 2 && $argv[1] == '--help') {
    printf("USAGE:\n  php7.4 parse.php <input >output\n  php7.4 parse.php [arguments]" .
        "\n\nARGUMENTS:\n  --help\tdisplay help\n");
    exit(0);
}
# no other arguments allowed
elseif ($argc != 1) {
    exit(10);
}

#### code parsing ####
$code = [];
# loop reads input and writes to $code
while ($line = fgets(STDIN)) {
    # skips empty lines and comments
    if (($line = preg_replace('/(^\s*$|^\s*#.*$|\s*#.*$)/','', trim($line))) != '') {
        $line = preg_replace('/\s+/', ' ', $line); # trim multiple whitespace chars to one
        $code[] = $line;
    }
}

# missing or invalid header
if ((count($code) == 0) || (strtolower($code[0]) != $header)) {
    exit(21);
}
else {
    # start and prepare new DOMDocument instance $doc for output
    $doc = new DOMDocument('1.0', 'UTF-8');
    $doc->formatOutput = true;

    $root = $doc->createElement('program');
    $root->setAttribute("language", "IPPcode21");
    $root = $doc->appendChild($root);
}

# if no more code
if (count($code) <= 1){
    print $doc->saveXML();
    exit(0);
}
$type = ""; # type of argument
$value = ""; # value of argument
# loop over all instructions
for ($i = 1; $i < count($code); $i++) {
    $line = explode(' ', $code[$i]);
    # check instruction validity
    if (!array_key_exists(strtolower($line[0]), $instructions)) {
        exit(22);
    }
    else {
        # if valid add instruction to $doc
        $elem = $doc->createElement('instruction');
        $elem->setAttribute("order", $i);
        $elem->setAttribute("opcode", strtoupper($line[0]));
    }
    $types = $instructions[strtolower($line[0])];
    $type_arr = str_split($types); # expected arguments
    # check if count of supplied arguments is valid
    if ((count($line) - 1) != (strlen($types))) {
        exit(23);
    }
    # loop over all arguments of one instruction
    for ($j = 0; $j < (strlen($types)); $j++) {
        switch ($type_arr[$j]) {
            case 'v':
                if (!is_variable($line[$j + 1]))
                    exit(23);
                $type = "var";
                $value = $line[$j + 1];
                break;
            case 's':
                if (!is_variable($line[$j + 1]) && !is_constant($line[$j + 1]))
                    exit(23);
                if (is_variable($line[$j + 1])) {
                    $type = "var";
                    $value = $line[$j + 1];
                } else {
                    [$type, $value] = explode("@", $line[$j + 1]);
                }
                break;
            case 'l':
                if (!is_label($line[$j + 1]))
                    exit(23);
                $type = "label";
                $value = $line[$j + 1];
                break;
            case 't':
                if (!is_type($line[$j + 1]))
                    exit(23);
                $type = "type";
                $value = $line[$j + 1];
                break;
        }
        # add argument to $doc
        $attr = $doc->createElement('arg' . ($j + 1), htmlspecialchars($value));
        $attr->setAttribute("type", $type);
        $elem->appendChild($attr);
    }
    $root->appendChild($elem);
}
print $doc->saveXML(); # print $doc to standard output
exit(0);