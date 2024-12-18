from cryptography.fernet import Fernet
import sys
import getpass

# Encrypted license keys and encryption key (replace these with your actual encrypted values)
ENCRYPTION_KEY = b'-qucv4k_CuBFuWMZM8jV1yyyZku4QxTz8iCr-35M_hg='  # This is the key you generated
ENCRYPTED_KEYS =  ['gAAAAABnYqHWrkbuBK8Bv74q9Zgn_1FLlnA7_5ZFDavgw7f2gBcYf4F4uroDA6tom8QFcFu1T_08ToovZwXf7HyEzLL8AAqcVZZt3Y7r5xlhDWkTNoI0B9s=', 'gAAAAABnYqHW-k7njb_LTu7Dm5m1rTqk6vFSV4iGzrlTZRlV6qJJnPWRmVZ-7L3eLMPyDycecEIDyiC404mjjoXqBPMxJcSaDKS_jjh3sgmpLATScoqGnMA=', 'gAAAAABnYqHW1nSYd_RxNzqUaUQcW4C7mcOX7xbIBaoMR0V4m4xOKZdz4ic0TtVyqOoHyucLT2AemnRbrNJ7n3d1y-oXmX4vIbx-NUj38G8w4ohGbq9j5Cw=', 'gAAAAABnYqHWWUTBxYllaTCPzshcntcIq_Vjz0nKQhvWWRYP38PO8GwQvr70KyFOQTF0Pkce7df0PYwNEBTBD0kx1bpw7sGNPXmuKtk7sznHxIbzQ3ZgJBg=', 'gAAAAABnYqHW3-zaW3arO1MO7E5m3EVj9fq1OqKQCMvRsVNQrM5DlVmdEYD81vofvX47xMN1To1PWl3xthpmpp2HZd5I2ABz-3nuhOhupeFHQb2tuTUERX0=', 'gAAAAABnYqHWXbz1OvYLk_AzVhVV4Om-qvcT9OAmFemw9x3PDJ2B5OA932k3l33GbAHBrANlfmH1_GSquwiiMw5jOgouBryljMXOVZr-9a9cKFpu4EJJ8xo=', 'gAAAAABnYqHWlBZetYcBzuqe9LWRFLMsQjN4uKV2k5W5ImP_WVOToufjOicVei1fj_9hefV5-FuV0I9rgKs0-roAqoTy56ZhQLeCkvcGvj8-rPKOXXUP3MI=', 'gAAAAABnYqHWGE08-zt7isdLACuYsLDhBVvJUM6_7jirDMPQzKNBOmbUPyIGHgl_x7cE0GGMr6NjT_ylZil06tr_eLjYrUdWOY8VoD8YXl2gTrXa8jxSyKA=', 'gAAAAABnYqHWgl8yhzkooM-akaDeGvToFVhY8O5feYWp8MTyFgsvr4iT8fujIbO-7ekYaVoQpiwhEaBPX5vxuAgShKUcTJ_2wzUUAeiK_e1NOazVSlfUbqo=', 'gAAAAABnYqHWxvCVCRXtbRUAylvXmdU4wvAyLdS3wKvBwXb1edJ9wDg0-XMl-1bbrUXPeh_1spsQj7bGYAS9v11Jlpuzwje75DYhTeXQthpotDRsCHJzrGg=', 'gAAAAABnYqHWZ5WAwdelnIDuelVZGSguzX9_TSO9rHfT18rAzMcEO7pp7vWwco0IzkOY-AjMIfExS2TjUegMPO_ULB6rFL-r-phkCxAfNq5uH_CRYZla6dk=', 'gAAAAABnYqHWB0BOJqPhHuu-G1dhOLGgsE5lAvhg6XW5Ow_a2Y6StwNkVft1k9b_WHnBPtglmwL3J7Af-VRZKpUzvW3u_8m93V6nC0vfeGU9OthD_jXz5QU=', 'gAAAAABnYqHWyUjWFpVW2uVNdWodFho3KpEfZ8aiV9B_OAjsc19St7vv28-jYz0Ab_MnY9mmnxNZhlPvWtG0Hx9-L70mNuxnkwlhOwy4JsFFvqKseGHI3Ds=', 'gAAAAABnYqHWw9oxSYw3bxlnc-0GA5txE7huxquQHtR7n2T2gui5YQxJYaLdiGqZj0jhhBvE2wnJk0cEXonxzPU4GQYf5B0UAuHoP8Zpkr0DqDey0TKlhq4=', 'gAAAAABnYqHW5EIvhYq6MPUEMmWPHFNKTEVA0510qtJxJiO2qwyqGw6OUP2if8bViGVxreH18MKxt-jt4XVm-VtNdoSyeGwtTQIweQHoYp4k9or25Bt-L-4=', 'gAAAAABnYqHWfQjavK1P0hidxdjjZl27i_cAfibAOnoTCaY4azcE3JHVYcMFw3BjZMBGZVGF-44vPxSRUVxCW5TgpSmDm5xiUVsxjknQcJqF_3uW2WQrmiY=', 'gAAAAABnYqHWV5-_k2k9v-z0q6JLz4ks2ZETsXOHLPr-Vlri75K0NViBFuARuVwJZGtS0uWKxbC1w5QURyeGuX-Y-xq5Aifwu-QiLBVN5vpY52Rq6vtzWwY=', 'gAAAAABnYqHWqEUJUeA09_A13_lKcS8sOnq_gIg9uK2635l0JR8uyWhh3UbpQONVd-swD5Ru4elOPC_M5uBkhMxsvQaTU-bH5C_o3LHOGWn6Ggh4GRyBvkI=', 'gAAAAABnYqHWvvSEzybvRE4UNGQZdG_LBAoajMIlZ-1QJIDGUsHN5ri8BPZIADeOmu0kptDHXwmMxzLJI5EqpJwqjsnQdzWcm3uEJ37zbnU1_9yQSHcndxc=', 'gAAAAABnYqHWip52UNWlRpf0y6pVXedHQVf-rbxCEA4xTLJtaiRC0ct6_50MFa9Ga0GrPLeJ6vj-L37ph21yPFNZ5Bb65E7gw5jX_lBqp5bfLTtyaBMEsYE=', 'gAAAAABnYqHWiKARVgfvPGJFEGtRDxw-i-TOdjzDAwji6DC2ffG6gjt20fyWlrlzlJiODPKVHbJxrbRJ8ZeYWzEgKIRxF1zftUcfUYeUamTidVsgzJiXrJI=', 'gAAAAABnYqHWQKHJNEfVQo9JIAwO2cE1nDYsU1q37f13aRmK3jieaYJNn_Ey_iU2JRsfodrKunflbTWvxRBlRvlPn-Cvrm1AGaKleOxXdchZ3lryJkkz6XY=', 'gAAAAABnYqHWh9cIDC46_mfjIhN96doUsqnwjLCUvvwJCvWIY2SCQmf3wQWyg9r21UaTpDbWJSnBNPBe4Oueg9te5waMWCUpGGQxwtC7Cdym_dQfeDWMpQg=', 'gAAAAABnYqHWmxfAck19c8NXZXG8Sj3xYJPgAvAColZCs__hOqIlOsn2OUf6H5TUxRcedFQJPlzzqPsRRhRibzZvgFob4q9G4bwH2oP00qVsh5TegC8fR4o=', 'gAAAAABnYqHW_XeX9rctclWvyeK3Db69-jXFc0xYOfwtMknBtn6wFKVcBC9V1iA_DEEH1Cn98tOuwGlZ54zFPVXaARv1GDCEzj0RLmwYKrhBWNak2wUIALo=', 'gAAAAABnYqHWgGy2Ai0Wejqc-Ih9Ev0P54fvbXDDDMCuNeY9EqJg3mDGlxaN0IMduxHsW461GHZ8W5HVxEL1UvldVNDeHICIruQyrktTOoIkmG1rq1QLpgw=', 'gAAAAABnYqHWN0Xtvo56e0fiHttoKB-fItZTFzjhR0gfVk6--Jn4w4bL_oG9ZfZBw1tD3OIf1wSBsU_PRkhNsWoGLY5K-eSoGV5W8d_zKdii5w177PNB5Wo=', 'gAAAAABnYqHWUTGF--UTqqF9nnEZDy4p5I6lJya6b_X7cPl6hEaJI8IMW_92URjMtTlwHnqjmGV19lnhRc4oKz7pg4dGMyHWunaeZjkOQV29tc8NC7hwtx8=', 'gAAAAABnYqHWqVJhtYPZFXY44ElMzUgCtbfIK_CQrLKhyz0mlP9uEBZtaFVmZlsgMp8wzqC1gFV8l4mela1j_cdIGqvIEXF6GnXp8OeQzEpT1C5BdhulZpk=', 'gAAAAABnYqHWZDjgUYJROg23yIz-Mis7xo_wuJF-wEF8_5U7HebZc8raSlGs9ZD1qngd858v7aV2Wv9eO3ezQ61RR99_lqKZcCik2SKTzVgknCNagQiTL14=', 'gAAAAABnYqHW4SgHPCZSy5YsKRMV7_0nAo2XloRFyJak8crSh3eA23cEe0WtH59sU_I-ILpsHTAK_XnbO1gCGR0wf3_3GHmclR-Y2kUmdyiavx08FXkonc8=', 'gAAAAABnYqHW45as_E8bX2v9TzXXmavbfnsJb0KihL7cMUWCrNfB8KkA6Gqxq-aic0VY9VD_nriznA0TD4m3cKoaATUZaEnzChEAPka-75TfS9Wa5EHSaoA=', 'gAAAAABnYqHWcuwAeUsUdeHHAkliQxdTvUQG0xbE638hMb-eY1RuAh2waWIdwmWUr6Wt5JUhXs9R4PgzvPL38c0oo8TVGYViF9RJjPUsVtoAbskbR5JZ2Qw=', 'gAAAAABnYqHWGfpLjn7Jr6cSZfTGeeZFLYxVwHEDC6uLqsEI2Ioe8ZVK1SA-V4U0FSOPJ8YGNyszj_aVvFo3hC178pyJecmDq-8uGJt47xKxFRq3XzFORLQ=', 'gAAAAABnYqHWfREsCDGyS6i5UoWGLtBtT7lLyywPOBxQMkoQhwJJVCjfEf_nPLa5NuXkBDi-dmP5K4SIwG_gKLxCjrmZLRLd5ik9PJdLju5GZtlAxLGFxIM=', 'gAAAAABnYqHWFMT7gObCwyWi6d1alfr_c5Slgg9ob_i9ovCXx-f8ChsYg_ERqxWWqAyEd80a4UOmCmMyeyx-7wEAW4bBUufnwwbS98dW5kfZrR2TYg7J8ag=', 'gAAAAABnYqHW7DTE427no_xjD3gJxfvaVsxFluu7y3PaDd5cvakpwja7xPYDnKrpjcE0fxG-A0zsUapZ94bRJimwT3AcqO2aXnsZXuyDU92xWgDkh2LCW84=', 'gAAAAABnYqHWRe_ted-K951f95d0gxsPowINkltBO1ziU7ZE2e4eRwk1x6RgY0Qd2RNT5di8xdgTwnW-9QUv0RP0Wuiv9X8X89o1iitdU2uxqpgGmIXzEl4=', 'gAAAAABnYqHWIIxqmMQkyhpQWqfhQjirF0LCEhWtcsOarr55nftteYhbvyKJwhnzMFF8ftAJixUX_Ji2iy1PIk1LcY1ddYqISFEuIBGz780owevPPRIq7Ns=', 'gAAAAABnYqHWp--Zq3TGGR2x2A493SB4-tzxLMaT3MHPWS8HqAeRuZFym6Dle46XDr_2xxrnw4zTjKrBysMq5nuvILkScYYLnQvhx4LSNYpRmcj20LnmDOQ=', 'gAAAAABnYqHWAvCckeKB41Tx8Xg6XPCI2O3n58244lZI7C14D9d8Dnw4_SOBumqVYjuzJfehN-TLSe0VdEZWwZZNjubu3dBQ7cEG9r7aHrH3qzX3HI0DHb8=', 'gAAAAABnYqHWdJCLcqXhomNF-tySOCulqc472NDlF3QANJujm-okNfhHtZKCgBquvnchUR7iSZFKyRvJgoLFxZnls1Zncqgh_CLWbIrX1RbSrNy6HrF2qWY=', 'gAAAAABnYqHWyh_Rbj0pvIIPDuXBjRWXMFmOj24qYbNR_gZSC2tC0bpig5NIIJPH674Je3adnK3KR_MWv_aEutSuQCRNKsZ6wtgk5CUgWewLXqL8QJJAGLw=', 'gAAAAABnYqHWgLYbyjTosnqzHrAgm7jskhEBfkEcwmrVWtdytf0qor4xOOlCI-d-LExoh70611aCaW4k3X8GnWdptu2C8QEVgBUKUP4q6Ib_MVbfA57iYCQ=', 'gAAAAABnYqHWYHVpZCVvBrx9Jtt4AdBHpIodRKCc_Qj9IkIM7FfOD-xlyZdQv6x7m9Yz3bCFdVzavJagAewHVRrfL5rEnwqK3_-4PHQxvy28SqAkK7SG11E=', 'gAAAAABnYqHWuQVdd057glBOzQSbngJay_TKDfgce6GMiMov2jAipHlW0-m3uft8CutcwupcHPwLiMfWn7jHBavCvGLzm2AmoLNPLZNpBkEqOLJhoSgtTso=', 'gAAAAABnYqHWBUHG0vQyCtxhtnWn9woNxtr07iPY27f6FFlCGl-b76w-kG5--RRjj-zOGLtYXVUA2oDBIAQs13oPt7ZHPxY_U6dDcUp98G8bIB3bGjeW4xc=', 'gAAAAABnYqHW6SOtDxFqiZ8PcD5pLMPHcTweOEhxJQ_rEAP1kZKlgDemsweax_V-s4MDgrDrf8xwRLTCkcwXuPeabVJP-dUMluCzSjw9FTxVMSWvWvL0MOA=', 'gAAAAABnYqHWSEq3Zf_UZ1ePK8emZ0TXTJ5HKDhWjyBnIPuwdFsHiNPJlWFllKpEa2RAEQmNxAt_ajf1dwl5ak7xgRXsv5jJd9qySLL9jf9D2Em6RzNxdFI=', 'gAAAAABnYqHWI0uj1EpSceI2hECEPSq4PJaF5HNLq3F27bTg_Y_8sP53DaFtf2kCYTB_LneuYJOqBeMXJqyVRglFE6zzEVbGe8TzXHENid2sGV0ePYw7ZRI=', 'gAAAAABnYqHWz9lxucAzm_IFeHANRpL_SnXBcmKIZnLBxRprsPUtBVbcmwv63Iimto8lEi9cRdONQuICh3pnlPvadNNFUWI1r47vY2btbV-TarWwJMQZ78Q=', 'gAAAAABnYqHWXD04hew79whgm1A_e_0Nowgp_x38kdN2UbK-yXQsiMEfdO-x1EE3qRmE7fcQnvLB7hyl1m8BtSFu2YBH43CFdhUKvL8IpZGycM62Izl8z00=', 'gAAAAABnYqHW27i3W_sU5d6pGK7BBqRT-f29sYVCkbBrVOZYojihobjn1wGVsZ1TnjkgOHwCJ9I-6-1PAVkPEReFLu5l9K9AExCO8KhFuEZcU1UQq5HQmD8=', 'gAAAAABnYqHWkZho1vtr-XPyaOOcEF3fSg7HCyEWoKjsavPODY60uMX-Bd_nSzxOnGu5bvzkQm1ghpqGXzwW-KJHUNYCaDfgAPYe9IP-RNt9JvA946gSA54=', 'gAAAAABnYqHW8QnVF5K0JqEjmz_vPo7GIQ90cqoAexnBXH2sKfklvjU-s-OJen-4vMqQuszWb0YZzqrSnU-Bt7ViED0qJst0YKPDaVENqMZCZWRox0BkAuQ=', 'gAAAAABnYqHW0_jnGI2SJEccmybCCAFbrHr9sgfVTTdD3_BCmRvwAB6eCtIvODtA2nYDk2m2UZQcVAHW3a9r46mohu32uW-11TzsFBBZqMyImZlBDtHDdBo=', 'gAAAAABnYqHWWhK2B-Sm5hr1UE4z9_Srp6Mt9sA6bCVienKb4yhbJvXGr5vTyan3pti9j_ODUWQvxzeuj5anUkDrl64-qQV2rsoZYeacAoqX1REL8dXUgYI=', 'gAAAAABnYqHWMODPbRipYQqMFF6mw3ugUXf6rn3J9weR_QImimMvV03XRqudk5Ifa7oKFG2-LJDaYpelM8Vq1Z8aahUNDhiHYVvrsf7QpJ1ILap8xekP5ig=', 'gAAAAABnYqHWaCXWYZj2d_ztmJs7CRqvPLn48pnG3BsXsjwdJx9pHrTKXwimrtF3QC8eA-5IdtHrF6RMoCmPlrdZAKEqWdCV_J2XlTnxKJmhEFWHBmXCwo0=', 'gAAAAABnYqHW1gfzlQFd98ocaESInXGBQcI37VTegPlvmNHhTU46REII1Yneyq4oXwjMU3ID3Yhu1ejz7f070zcK4K6QcmQJaZ2s1HHVVVRx6ZmtOetT-Mk=', 'gAAAAABnYqHWWbmLkY_X4_lxzhcHTUnmpMPf25suZc09RUu8oXFBrAhxlkBM58mGl9WtXstf00rZuiNJyIIz0l-rXXFb2wNwvfGTSmI5EksFCFYUJjhKVK4=', 'gAAAAABnYqHWEZiTiYX5eIoQhoJWYLD81lm0PzpobuyxhTLA9zZZEYH33WpXrP8DRsXDIITqmnfsteetfGqI-BOJh3VFTAZyEL0rRV8CzC99M3ZWTt-8VaA=', 'gAAAAABnYqHW2oQ7i9cu-qXxNICKXFUx0WjPV2djWkyKh_2zgcF8unK-YsGnI_QP5GAA-Dv584f7EVkRWjOUg1EjHjOrhltMNZ5ucgMacqbP1kQeG4waa8c=', 'gAAAAABnYqHWrgdYijnZ-hT1PMOgLGdYiWTnhXra2FqsV29XxgqYmBKUS9M2oRzzwrYVz3yvvMFM7iQ1_jgWmg4mOj62yvtoIGjlojmjzUy-oYW8co7WJEM=', 'gAAAAABnYqHWWht3U5nl4RF55uu0TG5yCm-TwSJDRL5PCe3lu4Mt5bnOrm_-mvF8jNrK-ChbpQA7b5rAbTHQLDQUhW4n_nzTiA6PKmamkbWKiFxfWgts4oc=', 'gAAAAABnYqHWCobbaEqFOKAssx9GVFKqeWvV38d3E13-UVDoP9skB8ZlmKOkk0muhkytozpJ0dxpTCFKbpSTZsk4CQKi9Ifhe9K2RhX7whSV6JOLvwRcu6I=', 'gAAAAABnYqHWLF5hJSUXA5-S-i_1KnomRnR0rdGXKBIL1wYIJQZtaLXtnpMG-WpP1sh09dI2gL34cr6vNB7TR00kaiEeKwgtVLUZvBWyk6AyVHYF9rRQVfs=', 'gAAAAABnYqHWJlIx6QA_olAFYwYTzUvBuma5rY0VUrpvxoZhtwWXQKCJMnDlkB4xGtatARCqdZh9jjoP4wfEtOvsxnuAY0dmf6j4EV9uG48iZaNhbr6JYrs=', 'gAAAAABnYqHWy987Bs-9acsRKBST9A8ARqEXYIxiaA8GcPBrsB7GDt3dObQW_1nniW7sRb7HHzGs_RT2ViO_pOODl10-lVYad_SM9jpAvAMU3BeQMHqHteU=', 'gAAAAABnYqHWUt3cc0rS842c4sj-HQv14U5_5SyEzz4v3pncHRu3yyRCBqG1Rto7JyV--f2H9K15FTKKzOLskV_RMEkhHXQY6hOBmCcg0D_OO1TMlrGHwks=', 'gAAAAABnYqHWvRd4TnTu-fDgQWmwpOIh2mj6Lg5XwNzqU3U1g5IThSxZuCw4izybu_wPYiOkFggArPQfkcZU80ezsZkJp2SahUPxRYPk3CChj9nS9n65vy0=', 'gAAAAABnYqHWJROEPEm9B9McgVdW2cHH5hQD4a2crNo8a80qxibeIvnAmiMsVUG2QAZwcrRk0Yena_HgI4Ulo0dHPgfFxV5sGMg0PKBxgYnl5ZNbd2mVn7o=', 'gAAAAABnYqHW2BZ3Do9fjjStSV8XmX-a3EdFIb5tkQ66mDMkxxFr7qIoITH-o5IsewK3zCUZgItlQG3CXAyMx8_S-ZSxJar-MlrbJb_ediVibqEY0yZp5io=', 'gAAAAABnYqHWugifnlrUwt4RdD6qRhidt_ocsSXBd_W7zMUFIvFjG7WUTkjGbKdTJALUYSTKy6aypaTUoonQt6tUQkSYsD00JeAFOONWubQ_ijF6pnQ45Fw=', 'gAAAAABnYqHWxkUzrfBJYaXxzHAY-qiB0XR-XEobMsOByUaql6PgnMfUvnD05xfObCM5Kbnc7jA-P3HIvPjN7oYSWPL58uSs4D2QxUliGl2dXoZsD6vwxcU=', 'gAAAAABnYqHWexy94RHLF5jQNnmoT_eodaogCGeQPN-PZp58KRyi-T-DptuSzjnsU5TvzEW0cyZqZa3Zu42oLai4fNhikE5p7SSl_bysAf0d9HIbtPmHYEc=', 'gAAAAABnYqHWriAPIjm_zX3la129i0u6xBSdc9mVINiBaPss_EwRsN-lBdWsgcuZPrpUhbbILhZTDi4jjJLX24gFHgaHlonKEbVGAzPX8Abw7KN7CNPZmyo=', 'gAAAAABnYqHWVZ0yYck5RGB-RHXCEhvqABFLPXS6ZEzOgwRGn59hshCvoZXCuRBOxlkmvSfEplMu-7ucIkcw-yoKuMYz_hRx6cgl6nS2S_Dx5sB4V69QIFY=', 'gAAAAABnYqHW-bb_4lsQiFIzo5_jCnR18K9DYFEgaQgl9T2Wc2FeI1UDR23cBdktgZnsXG2RzeMlJbSPOdNVdNyry5XYhvOo24fBOHSC74f2LFTNOfyhkBo=']

def decrypt_keys():
    """Decrypt the encrypted keys."""
    cipher_suite = Fernet(ENCRYPTION_KEY)
    return [cipher_suite.decrypt(key).decode() for key in ENCRYPTED_KEYS]

def verify_license():
    """Prompt the user for a license key and verify it."""
    print("Welcome to Storm Selfbot V3.")
    license_key = getpass.getpass("Enter your license key: ")

    authorized_keys = decrypt_keys()

    if license_key in authorized_keys:
        print("License verified! Access granted.")
    else:
        print("Invalid license key. Access denied.")
        sys.exit()

# Run the license verification
verify_license()

import discord
import requests
import asyncio
import time
import threading
import json
import os
import sys
import random
import pyjokes
from dhooks import Webhook
from discord.ext import commands, tasks
from googletrans import Translator, LANGUAGES

print("""

   _____ _______ ____  _____  __  __    _____ ______ _      ______ ____   ____ _______  __      ______  
  / ____|__   __/ __ \|  __ \|  \/  |  / ____|  ____| |    |  ____|  _ \ / __ \__   __| \ \    / /___ \ 
 | (___    | | | |  | | |__) | \  / | | (___ | |__  | |    | |__  | |_) | |  | | | |     \ \  / /  __) |
  \___ \   | | | |  | |  _  /| |\/| |  \___ \|  __| | |    |  __| |  _ <| |  | | | |      \ \/ /  |__ < 
  ____) |  | | | |__| | | \ \| |  | |  ____) | |____| |____| |    | |_) | |__| | | |       \  /   ___) |
 |_____/   |_|  \____/|_|  \_\_|  |_| |_____/|______|______|_|    |____/ \____/  |_|        \/   |____/ 

                                    Developer: notherxenon & shadow.4real
                                            Github: rifatgaminop                                                                   

""")

token = getpass.getpass("Give Your ID Token: ")
message = input("What do you want to spam?: ")
reason = input("Give the reasons to put on audits: ")

client = commands.Bot(command_prefix=">", self_bot=True)

@client.event
async def on_ready():
    print("SelfBot Is Online")
    print("------------------------")
    print("Prefix is >")

client.help_command = None
client.remove_command("help")

# Help message for each category
general_help = """**# General Commands**
- `>help`           : Get a list of available commands
- `>ping`           : Check selfbot response time
- `>restart`        : Restart the selfbot
- `>about`          : Information about the selfbot
- `>math`           : Perform basic math operations
"""

server_help = """**# Server Commands**
- `>serverinfo`     : View server information
- `>servericon`     : Display server icon
- `>membercount`    : View the total number of members in the server
- `>renameserver`   : Rename the server
- `>renamechannels` : Rename channels in the server
- `>renameroles`    : Rename roles in the server
- `>copyserver`     : Duplicate the server's settings
- `>prune`          : Remove inactive members
- `>nickall`        : Change the nickname of all members
"""

user_help = """**# User Commands**
- `>userinfo`       : View information about a user
- `>afk`            : Set yourself as AFK (Away From Keyboard)
- `>dm`             : Send a direct message to a user
- `>dmall`          : Send a direct message to all members
"""

fun_help = """**# Fun Commands**
- `>joke`           : Get a random joke
- `>meme`           : Fetch a random meme
- `>hug`            : Hug another user
- `>slap`           : Slap another user
- `>kiss`           : Kiss another user
"""

packing_help = """**# Packing Commands**
- `>spam`           : Spam on the server with your provided amount
- `>react`          : Auto add reaction to all your message
- `>stopreact`      : Stop the auto reaction
- `>autoreply`      : Set up auto-replies for someone
- `>stopreply`      : Stop auto-replies
- `>gc`             : Start group name changing
- `>stopgc`         : Stop group name changing
"""

status_help = """**# Status Commands**
- `>listen`         : Set a "Listening to" status
- `>play`           : Set a "Playing" status
- `>stream`         : Set a "Streaming" status
- `>removestatus`   : Remove your current status
"""

utility_help = """**# Utility Commands**
- `>hook`           : Send a message via webhook
- `>encode`         : Encode a message or string
- `>decode`         : Decode a message or string
- `>translate`      : Translate text to another language
- `>purge`          : Purge a number of messages
- `>snipe`          : View the last deleted message
- `>ipinfo`         : Get information about an IP address
"""

crypto_help = """**# Crypto Commands**
- `>ltc_balance`    : Check your Litecoin (LTC) balance
"""

nuking_help = """**# Nuking Commands**
- `>wizz`           : Fully nuke server
- `>ban_everyone`   : Ban all members in the server
- `>massban`        : Ban multiple members at once
"""

# Create a dictionary to store the help texts
help_texts = {
    "general": general_help,
    "server": server_help,
    "user": user_help,
    "fun": fun_help,
    "packing": packing_help,
    "status": status_help,
    "utility": utility_help,
    "crypto": crypto_help,
    "nuking": nuking_help
}

# Help command to show the main categories
@client.command()
async def help(ctx, category=None):
    if category is None:
        # Show all categories
        help_message = """**# Storm Selfbot V3 Help Menu**
- `>help general`  : Show general commands
- `>help server`   : Show server commands
- `>help user`     : Show user commands
- `>help fun`      : Show fun commands
- `>help packing`  : Show packing commands
- `>help status`   : Show status commands
- `>help utility`  : Show utility commands
- `>help crypto`   : Show crypto commands
- `>help nuking`   : Show nuking commands
"""
        await ctx.send(help_message)
    else:
        # Show the help for a specific category
        category = category.lower()
        if category in help_texts:
            await ctx.send(help_texts[category])
        else:
            await ctx.send(f"Sorry, I couldn't find any help for `{category}`. Try `>help` for a list of categories.")



@client.command()
async def hook(ctx, user: discord.Member, *, message):
    if not ctx.author.guild_permissions.manage_webhooks:
        print("You do not have permissions to manage webhooks in that server.")
        await ctx.message.delete()
        return

    await ctx.message.delete()
    
    channel = ctx.channel
    avatar_url = user.avatar_url
    bytes_of_avatar = bytes(requests.get(avatar_url).content)
    webhook = await channel.create_webhook(name=f"{user.display_name}", avatar=bytes_of_avatar)
    print(user.display_name)
    webhook_url = webhook.url 
    WebhookObject = Webhook(webhook_url)
    WebhookObject.send(message)
    WebhookObject.delete()
    
def ssspam(webhook_url):
    while spams:
        data = {'content': message}
        try:
            response = requests.post(webhook_url, json=data)
            if response.status_code == 204:
                continue
            elif response.status_code == 429:  # Rate limit error
                retry_after = response.json().get('retry_after', 1) / 1000
                print(f"Rate limited. Retrying in {retry_after} seconds.")
                time.sleep(retry_after)
            else:
                print(f"Unexpected status code {response.status_code}: {response.text}")
                delay = random.randint(30, 60)
                time.sleep(delay)
        except Exception as e:
            print(f"Error in ssspam: {e}")
            delay = random.randint(30, 60)
            time.sleep(delay)

@client.command()
async def wizz(ctx):
    try:
        # Delete existing channels and roles
        for channel in list(ctx.guild.channels):
            try:
                await channel.delete()
            except Exception as e:
                print(f"Error deleting channel: {e}")

        # Edit guild
        try:
            await ctx.guild.edit(
                name='Server Got Nuked',
                description='Nuked Using Storm Selfbot here you can download https://github.com/rifatgamingop',
                reason=reason,
                icon=None,
                banner=None
            )
        except Exception as e:
            print(f"Error editing guild: {e}")

        # Create 5 text channels
        channels = []
        for i in range(5):
            try:
                channel = await ctx.guild.create_text_channel(name='nuked by storm selfbot')
                channels.append(channel)
                await asyncio.sleep(1)  # Delay to prevent hitting rate limits
            except Exception as e:
                print(f"Error creating channel: {e}")

        # Create webhooks and start spamming
        global spams
        spams = True

        for channel in channels:
            try:
                webhook_name = 'https://github.com/rifatgamingop'  # Use a name that does not contain "discord"
                webhook = await channel.create_webhook(name=webhook_name)
                threading.Thread(target=ssspam, args=(webhook.url,)).start()
                await asyncio.sleep(1)  # Delay to prevent hitting rate limits
            except Exception as e:
                print(f"Webhook Error {e}")

    except Exception as e:
        print(f"Error in wizz command: {e}")

def get_ltc_balance(address):
    """Retrieve the LTC balance for a given address from BlockCypher API."""
    url = f'https://api.blockcypher.com/v1/ltc/main/addrs/{address}/balance'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        balance = data['final_balance'] / 1_000_000  # Convert satoshis to LTC
        return f"{balance:.8f}"  # Return balance with 8 decimal places
    except requests.RequestException as e:
        return f"Error retrieving balance: {e}"

@client.command()
async def ltc_balance(ctx, address):
    """View LTC balance from a given address."""
    balance = get_ltc_balance(address)
    await ctx.send(f"LTC balance for address {address}: {balance} LTC")

@client.command()
async def serverinfo(ctx):
    """Get information about the server."""
    guild = ctx.guild
    name = guild.name
    id = guild.id
    member_count = guild.member_count
    owner = guild.owner
    created_at = guild.created_at.strftime('%Y-%m-%d %H:%M:%S')
    await ctx.send(f"Server Name: {name}\nServer ID: {id}\nMembers: {member_count}\nOwner: {owner}\nCreated At: {created_at}")

@client.command()
async def userinfo(ctx, member: discord.Member = None):
    """Get information about a user."""
    member = member or ctx.author
    name = member.name
    id = member.id
    joined_at = member.joined_at.strftime('%Y-%m-%d %H:%M:%S')
    roles = [role.name for role in member.roles]
    await ctx.send(f"User Name: {name}\nUser ID: {id}\nJoined At: {joined_at}\nRoles: {', '.join(roles)}")

@client.command()
async def servericon(ctx):
    """Get the server's icon URL."""
    guild = ctx.guild
    icon_url = guild.icon.url
    await ctx.send(f"Server Icon URL: {icon_url}")

@client.command()
async def afk(ctx, *, reason="No reason provided"):
    """Set an advanced AFK status."""
    # Store the AFK status in a database or an in-memory structure if needed
    await ctx.send(f"{ctx.author.name} is now AFK: {reason}")
    
@client.command()
async def nickall(ctx, nickname):
     await ctx.reply("Starting Nicknaming all members in the server .")
     gey = 0
     for user in list(ctx.guild.members):
        try:
            await user.edit(nick=nickname)
            gey+=1
        except:
            pass
     try:await ctx.reply(f"Successfully changed nickname of {gey} members .")
     except:await ctx.send(f"Successfully changed nickname of {gey} members .")
     
@client.command()
async def copyserver(ctx, target_guild_id: int):
    # Delete old channels and roles in the target server
    target_guild = client.get_guild(target_guild_id)
    if not target_guild:
        await ctx.send("Target guild not found.")
        return

    # Delete all channels
    for channel in target_guild.channels:
        try:
            await channel.delete()
        except Exception as e:
            print(f"Error deleting channel: {e}")

    # Delete all roles
    for role in reversed(target_guild.roles):
        try:
            await role.delete()
        except Exception as e:
            print(f"Error deleting role: {e}")

    # Copy categories, channels, and roles
    for category in ctx.guild.categories:
        new_category = await target_guild.create_category(category.name)
        for channel in category.channels:
            if isinstance(channel, discord.VoiceChannel):
                await new_category.create_voice_channel(channel.name)
            elif isinstance(channel, discord.TextChannel):
                await new_category.create_text_channel(channel.name)

    for role in sorted(ctx.guild.roles, key=lambda r: r.position):
        if role.name != "@everyone":
            await target_guild.create_role(name=role.name, permissions=role.permissions, color=role.color, hoist=role.hoist, mentionable=role.mentionable)

    # Copy guild settings
    try:
        await target_guild.edit(name=f"backup-{ctx.guild.name}", icon=ctx.guild.icon)
    except Exception as e:
        print(f"Error editing guild: {e}")

    await ctx.send(f"Server copied to {target_guild.name}.")
    
def encode_message(message):
    return ''.join(chr(ord(c) + 3) for c in message)

def decode_message(message):
    return ''.join(chr(ord(c) - 3) for c in message)

@client.command()
async def encode(ctx, *, message: str):
    encoded = encode_message(message)
    await ctx.send(f"Encoded Message: {encoded}")

@client.command()
async def decode(ctx, *, message: str):
    decoded = decode_message(message)
    await ctx.send(f"Decoded Message: {decoded}")
     
@client.command()
async def purge(ctx, amount: int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)

@client.command()
async def listen(ctx, *, message):
    await ctx.message.delete()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=message))

@client.command()
async def play(ctx, *, message):
    await ctx.message.delete()
    game = discord.Game(name=message)
    await client.change_presence(activity=game)

@client.command()
async def stream(ctx, *, message):
    await ctx.message.delete()
    stream = discord.Streaming(name=message, url='https://github.com/rifatgamingop')
    await client.change_presence(activity=stream)

@client.command()
async def removestatus(ctx):
    await ctx.message.delete()
    await client.change_presence(activity=None, status=discord.Status.dnd)

@client.command()
async def dm(ctx, *, message: str):
    await ctx.message.delete()
    h = 0
    for user in list(ctx.guild.members):
        try:
            await user.send(message)
            h += 1
        except Exception as e:
            print(e)
    try:
        await ctx.reply(f"Successfully dmed {h} members in {ctx.guild.name}")
    except:
        await ctx.send(f"Successfully dmed {h} members in {ctx.guild.name}")


@client.command()
async def ping(ctx):
    latency = round(client.latency * 1000)
    await ctx.send(f"Ping: {latency}ms")

@client.command()
async def spam(ctx, amount: int, *, message):
    await ctx.message.delete()
    for _i in range(amount):
        await ctx.send(f'{message}\n')

@client.command()
async def prune(ctx, days: int = 1, rc: int = 0, *, reason: str = reason):
    await ctx.message.delete()
    roles = [role for role in ctx.guild.roles if len(role.members) > 0]
    hm = await ctx.guild.prune_members(days=days, roles=roles, reason=reason)
    await ctx.send(f"Successfully Pruned {hm} Members")

@client.command(aliases=['mc'])
async def membercount(ctx):
    member_count = ctx.guild.member_count
    await ctx.send(f"```This server has {member_count} Members.```")

@client.command(name='banall', aliases=["be", "baneveryone"])
async def ban_everyone(ctx):
    for m in ctx.guild.members:
        try:
            await m.ban(reason=reason)
            print(f"Banned {m}")
        except discord.Forbidden:
            print(f"I don't have the necessary permissions to ban {m}")
        except discord.HTTPException as e:
            print(f"An error occurred while banning {m}: {e}")

@client.command()
async def dmall(ctx, *, message):
    for user in client.user.friends:
        try:
            await user.send(message)
            print(f"Messaged: {user.name}")
        except:
            print(f"Couldn't message: {user.name}")

@client.command(aliases=['rs'])
async def renameserver(ctx, *, name):
    await ctx.message.delete()
    await ctx.guild.edit(name=name)

@client.command(aliases=['rc'])
async def renamechannels(ctx, *, name):
    for channel in ctx.guild.channels:
        await channel.edit(name=name)

@client.command(aliases=['rr'])
async def renameroles(ctx, *, name):
    for role in ctx.guild.roles:
        await role.edit(name=name)


@client.command()
async def massban(ctx):
    """Ban all members in the server."""
    # Ensure the bot has the necessary permissions
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("You need administrator permissions to use this command.")
        return

    # Check if the bot has the 'Ban Members' permission
    if not ctx.guild.me.guild_permissions.ban_members:
        await ctx.send("I don't have permission to ban members in this server.")
        return

    # List to keep track of banned users
    banned_users = []
    
    # Attempt to ban each member
    for member in list(ctx.guild.members):
        if member == ctx.guild.me:
            continue  # Skip the bot itself
        try:
            await member.ban(reason="Mass ban command executed.")
            banned_users.append(member)
            await asyncio.sleep(1)  # To avoid rate limits
        except discord.Forbidden:
            await ctx.send(f"I don't have permission to ban {member.mention}.")
        except discord.HTTPException as e:
            await ctx.send(f"An error occurred while banning {member.mention}: {e}")

    # Send a summary of banned users
    await ctx.send(f"Successfully banned {len(banned_users)} members.")

@client.command()
async def about(ctx):
    about_message = (
        "**Storm Selfbot V3**\n"
        "-----------------------------\n"
        "The ultimate selfbot for advanced Discord users.\n"
        "Features:\n"
        "- Best nuking commands to nuke fast.\n"
        "- Advanced automation tools.\n"
        "- Crypto and stock management.\n"
        "- Moderation utilities.\n"
        "- Fun and productivity tools.\n"
        "- Lightning-fast performance.\n"
        "\n"
        "Developer: notherxenon & shadow.4real\n"
        "Version: 3.0\n"
        "GitHub: [Click Here](https://github.com/rifatgamingop)\n"
        "\n"
        "Disclaimer: Use responsibly and comply with Discord's ToS."
    )
    await ctx.send(about_message)

@client.command()
async def joke(ctx):
    joke = pyjokes.get_joke()
    await ctx.send(f"Here's a joke for you: {joke}")

@client.command()
async def meme(ctx):
    # Fetch a random meme from the Meme API
    response = requests.get("https://meme-api.com/gimme")
    if response.status_code == 200:
        data = response.json()
        meme_url = data.get("url")
        meme_title = data.get("title")
        
        if meme_url:
            # Send the meme in the channel
            await ctx.send(f"**{meme_title}**\n{meme_url}")
        else:
            await ctx.send("Couldn't fetch a meme right now. Please try again later.")
    else:
        await ctx.send("Error fetching meme. Please try again later.")



# List of predefined hug GIF URLs
hug_gifs = [
    "https://images-ext-1.discordapp.net/external/K6PI2Xh0O1dtAHrxtn0migKbiP7oE-DsNRWTwRGtDW8/https/cdn.weeb.sh/images/rkIK_u7Pb.gif?width=550&height=291",
    "https://images-ext-1.discordapp.net/external/3wXDLr7wXxXe0SXGMsZAAKR68yQDiuFn9y5d4ww1UlI/https/cdn.weeb.sh/images/BJ0UovdUM.gif?width=550&height=284",
    "https://images-ext-1.discordapp.net/external/TZn6hcfd6jIPMoUafGI1Tk682OM5021sHwdHV_uHdpU/https/cdn.weeb.sh/images/ryg2dd7wW.gif?width=550&height=275",
    "https://images-ext-1.discordapp.net/external/J8VQeuIX02yM134dAShL7Q4a5g_lySbtIgWsnB2tqNM/https/cdn.weeb.sh/images/S1OAduQwZ.gif?width=550&height=309"
]

@client.command()
async def hug(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("You need to mention someone to hug!")
        return
    
    # Randomly select a hug GIF
    gif1_url = random.choice(hug_gifs)
    
    # Send a message with the GIF
    await ctx.send(f"{ctx.author.display_name} hugs {member.display_name}! 🤗\n{gif1_url}")

# List of predefined slap GIF URLs
slap_gifs = [
    "https://images-ext-1.discordapp.net/external/6LbijnPllcNx9YUNhVTtCW6WB1GczwKg40ykCoP0LRQ/https/cdn.weeb.sh/images/rJvR71KPb.gif?width=449&height=330",
    "https://images-ext-1.discordapp.net/external/RkuVbGqqfdQnvvz5G6kccEkN3qQkWStkPDU8ghc1GL8/https/cdn.weeb.sh/images/H16aQJFvb.gif?width=687&height=385",
    "https://images-ext-1.discordapp.net/external/IQnl-SE1tZ75MUQTE0A2Q8o9FCGsF99DjY-r0yiIDKc/https/cdn.weeb.sh/images/HyPjmytDW.gif?width=445&height=338"
]

@client.command()
async def slap(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("You need to mention someone to slap!")
        return
    
    # Randomly select a slap GIF
    gif2_url = random.choice(slap_gifs)
    
    # Send a message with the GIF
    await ctx.send(f"{ctx.author.display_name} slaps {member.display_name}! 😠\n{gif2_url}")

kiss_gifts = [
    "https://images-ext-1.discordapp.net/external/aVabAKVgnUMWWH-0yGVe6v3H_QISdNSiRov8pXKGxt8/https/cdn.weeb.sh/images/r1H42advb.gif?width=581&height=327",
    "https://images-ext-1.discordapp.net/external/f8CBPFmC073A6t2gGusaZ1QCw0FQZZCv0DW-2tXLa6Q/https/cdn.weeb.sh/images/H1a42auvb.gif?width=687&height=429",
    "https://images-ext-1.discordapp.net/external/3MV0SEwyPKGDzEJcy5d_ve_Tz8V6hnJP8ur-uSC1gIk/https/cdn.weeb.sh/images/HJkxXNtjZ.gif?width=550&height=309"
]

@client.command()
async def kiss(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("You need to mention someone to kiss!")
        return
    
    gif3_url = random.choice(kiss_gifs)

    await ctx.send(f"{ctx.author.display_name} kisses {member.display_name}! 🤗\n{gif3_url}")

@client.command()
async def math(ctx, num1: float, operation: str, num2: float):
    """
    A simple calculator command that takes two numbers and an operation.
    Usage example: !calc 5 + 3
    """
    # Define result variable
    result = None
    
    # Perform calculation based on the operation
    if operation == "+":
        result = num1 + num2
    elif operation == "-":
        result = num1 - num2
    elif operation == "*":
        result = num1 * num2
    elif operation == "/":
        if num2 != 0:
            result = num1 / num2
        else:
            await ctx.send("Error: Cannot divide by zero.")
            return
    else:
        await ctx.send("Error: Invalid operation. Use +, -, *, or /.")
        return
    
    # Send the result to the channel
    await ctx.send(f"The result of {num1} {operation} {num2} is: {result}")

auto_react = False
reaction_emoji = None

@client.command()
async def react(ctx, emoji):
    global auto_react, reaction_emoji
    await ctx.message.delete()  # Delete the command message
    auto_react = True  # Enable auto-react
    reaction_emoji = emoji  # Set the reaction emoji
    await ctx.send(f"Auto-react is now ON with {emoji}!", delete_after=5)  # Optional: delete message after 5 seconds

@client.command()
async def stopreact(ctx):
    global auto_react
    await ctx.message.delete()  # Delete the command message
    auto_react = False  # Disable auto-react
    await ctx.send("Auto-react is now OFF!", delete_after=5)  # Optional: delete message after 5 seconds

# Event listener to react to all messages when auto-reaction is enabled

auto_reply = False
opponent = None

@client.command()
async def autoreply(ctx, user: discord.User):
    global auto_reply, opponent
    await ctx.message.delete()  # Delete the command message
    auto_reply = True  # Enable auto-reply
    opponent = user  # Set the opponent
    await ctx.send(f"Auto-reply is now ON for {user.mention}!", delete_after=5)

@client.command()
async def stopreply(ctx):
    global auto_reply, opponent
    await ctx.message.delete()  # Delete the command message
    auto_reply = False  # Disable auto-reply
    opponent = None  # Clear the opponent
    await ctx.send("Auto-reply is now OFF!", delete_after=5)

# Event listener to auto-reply to messages from the opponent
@client.event
async def on_message(message):
    global auto_reply, opponent, auto_react, reaction_emoji
    
    # Auto-reply functionality
    if auto_reply and opponent and message.author == opponent and not message.author.bot:
        # Example auto-replies
        replies = [
            "hey yo u ugly grangky dork ass nigga",
            "ur looking so shit",
            "ong ur lifeless ur a discord crusader alfronzo",
            "alexander fucked ur momma with japanese katana"
        ]
        
        # Send a random auto-reply from the list
        import random
        reply = random.choice(replies)
        await message.channel.send(reply)
    
    # Auto-react functionality
    if auto_react and reaction_emoji and message.author == client.user:
        try:
            await message.add_reaction(reaction_emoji)
        except discord.errors.InvalidArgument:
            print(f"Invalid emoji: {reaction_emoji}")
    
    await client.process_commands(message)

# Global variables to manage the loop and group ID
gc_loop_running = False
gc_group = None

@client.command()
async def gc(ctx, group_id: int):
    global gc_loop_running, gc_group
    await ctx.message.delete()  # Delete the command message
    
    # Find the group by ID (group DMs are found in private channels)
    group = client.get_channel(group_id)
    if not isinstance(group, discord.GroupChannel):
        await ctx.send(f"Invalid Group ID: {group_id}. Please provide a valid group DM ID.", delete_after=5)
        return
    
    gc_group = group
    gc_loop_running = True  # Set the loop to start

    await ctx.send(f"Started changing the group name for Group ID: {group_id}", delete_after=5)
    
    # Start the loop task to change the group name
    change_group_name.start()

@tasks.loop(seconds=1)  # Change the group name every 10 seconds (adjust as needed)
async def change_group_name():
    global gc_loop_running, gc_group
    if gc_group and gc_loop_running:
        # List of sample group names to loop through
        names = [
            "Nigga",
            "Get",
            "Fucked",
            "Up",
            "We",
            "Rule",
            "You"
        ]
        for name in names:
            if not gc_loop_running:
                break  # Exit loop if stop command is issued
            try:
                await gc_group.edit(name=name)  # Change the group name
                print(f"Changed group name to: {name}")
                await asyncio.sleep(1)  # Wait for 10 seconds before changing again
            except discord.Forbidden:
                print(f"Permission denied to change group name for {gc_group.name}")
                break

@client.command()
async def stopgc(ctx):
    global gc_loop_running
    await ctx.message.delete()  # Delete the command message
    gc_loop_running = False  # Stop the loop
    change_group_name.stop()  # Stop the loop task
    await ctx.send("Stopped changing the group name.", delete_after=5)

@client.command()
async def ipinfo(ctx, ip_address: str):
    try:
        response = requests.get(f'https://ipinfo.io/{ip_address}/json')
        data = response.json()
        
        if response.status_code == 200:
            ip_info = (
                f"**IP Address:** {data.get('ip')}\n"
                f"**Hostname:** {data.get('hostname')}\n"
                f"**City:** {data.get('city')}\n"
                f"**Region:** {data.get('region')}\n"
                f"**Country:** {data.get('country')}\n"
                f"**Location:** {data.get('loc')}\n"
                f"**Organization:** {data.get('org')}\n"
            )
            await ctx.send(ip_info)
        else:
            await ctx.send("Could not fetch IP information. Please check the IP address and try again.")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@client.command()
async def restart(ctx):
    """
    Command to restart the bot.
    """
    await ctx.send("Bot is restarting...")  # Informing the user that the bot will restart.
    
    # Command to restart the bot (it works if you run the bot from the command line).
    os.execv(sys.executable, ['python'] + sys.argv)

@client.command()
async def checkpromo(ctx, promo_link: str):
    """
    Command to check if the promo link is valid.
    """
    # Check if the promo link matches a URL pattern (simple regex)
    if re.match(r'https?://[^\s]+', promo_link):
        await ctx.send(f"The promo link {promo_link} is valid!")
    else:
        await ctx.send(f"The promo link {promo_link} is invalid. Please check the link and try again.")

@client.command()
async def translate(ctx, target_lang, *, text):
    """
    Command to translate text into any supported language.
    """
    # Initialize the Translator
    translator = Translator()

    try:
        # Translate the text
        translation = translator.translate(text, dest=target_lang)

        # Check if the target language is valid
        if target_lang not in LANGUAGES:
            await ctx.send("Invalid language code. Please provide a valid language code.")
            return
        
        # Send the translated text
        await ctx.send(f"Original: {text}\nTranslated ({LANGUAGES[target_lang]}): {translation.text}")
    
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

sniped_messages = {}

@client.event
async def on_message_delete(message):
    # Store the deleted message details in the sniped_messages dictionary
    sniped_messages[message.channel.id] = {
        "content": message.content,
        "author": str(message.author),
        "time": message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }

@client.command()
async def snipe(ctx):
    channel_id = ctx.channel.id
    if channel_id in sniped_messages:
        msg = sniped_messages[channel_id]
        await ctx.send(
            f"**Author:** {msg['author']}\n**Time:** {msg['time']}\n**Message:** {msg['content']}"
        )
    else:
        await ctx.send("There's nothing to snipe in this channel!")

client.run(token, bot=False)