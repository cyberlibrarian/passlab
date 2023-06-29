# Exercise 7
## Cracking Passwords with Rules

```
hashcat.bin -O -m 1000 --username -a 0 -r rules/best64.rule ntlm.txt words/rockyou.txt.gz
```

## Rules that come with Hashcat
Listed from biggest to smallest ruleset

- dive.rule
- generated2.rule
- rockyou-30000.rule
- Incisive-leetspeak.rule
- d3ad0ne.rule
- T0XlCv2.rule
- T0XlC_insert_HTML_entities_0_Z.rule
- generated.rule
- T0XlC-insert_00-99_1950-2050_toprules_0_F.rule
- unix-ninja-leetspeak.rule
- toggles5.rule
- InsidePro-HashManager.rule
- T0XlC.rule
- T0XlC-insert_top_100_passwords_1_G.rule
- InsidePro-PasswordsPro.rule
- toggles4.rule
- toggles3.rule
- T0XlC-insert_space_and_special_0_F.rule
- specific.rule
- oscommerce.rule
- T0XlC_3_rule.rule
- best64.rule
- combinator.rule
- toggles2.rule
- leetspeak.rule
- toggles1.rule

## Other ruleset to download

- OneRuletoRuleThemAll
- KoreLogic
- NSA Rules
- Hob0Rules
