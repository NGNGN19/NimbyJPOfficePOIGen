def zenkaku_replace(item:str):
    sapporo = False
    asahikawa = False
    sakai = False

    item = item.replace("ヶ", "ケ")
    item = item.replace("二十一丁目", "２１丁目")
    item = item.replace("二十二丁目", "２２丁目")
    item = item.replace("二十三丁目", "２３丁目")
    item = item.replace("二十四丁目", "２４丁目")
    item = item.replace("二十五丁目", "２５丁目")
    item = item.replace("二十六丁目", "２６丁目")
    item = item.replace("二十七丁目", "２７丁目")
    item = item.replace("二十八丁目", "２８丁目")
    item = item.replace("二十九丁目", "２９丁目")
    item = item.replace("二十丁目", "２０丁目")
    item = item.replace("三十丁目", "３０丁目")
    item = item.replace("十一丁目", "１１丁目")
    item = item.replace("十二丁目", "１２丁目")
    item = item.replace("十三丁目", "１３丁目")
    item = item.replace("十四丁目", "１４丁目")
    item = item.replace("十五丁目", "１５丁目")
    item = item.replace("十六丁目", "１６丁目")
    item = item.replace("十七丁目", "１７丁目")
    item = item.replace("十八丁目", "１８丁目")
    item = item.replace("十九丁目", "１９丁目")
    item = item.replace("一丁目","１丁目")
    item = item.replace("二丁目","２丁目")
    item = item.replace("三丁目","３丁目")
    item = item.replace("四丁目","４丁目")
    item = item.replace("五丁目","５丁目")
    item = item.replace("六丁目","６丁目")
    item = item.replace("七丁目","７丁目")
    item = item.replace("八丁目","８丁目")
    item = item.replace("九丁目","９丁目")
    item = item.replace("十丁目","１０丁目")
    item = item.replace("10丁目", "１０丁目")
    item = item.replace("11丁目", "１１丁目")
    item = item.replace("12丁目", "１２丁目")
    item = item.replace("13丁目", "１３丁目")
    item = item.replace("14丁目", "１４丁目")
    item = item.replace("15丁目", "１５丁目")
    item = item.replace("16丁目", "１６丁目")
    item = item.replace("17丁目", "１７丁目")
    item = item.replace("18丁目", "１８丁目")
    item = item.replace("19丁目", "１９丁目")
    item = item.replace("20丁目", "２０丁目")
    item = item.replace("21丁目", "２１丁目")
    item = item.replace("22丁目", "２２丁目")
    item = item.replace("23丁目", "２３丁目")
    item = item.replace("24丁目", "２４丁目")
    item = item.replace("25丁目", "２５丁目")
    item = item.replace("26丁目", "２６丁目")
    item = item.replace("27丁目", "２７丁目")
    item = item.replace("28丁目", "２８丁目")
    item = item.replace("29丁目", "２９丁目")
    item = item.replace("30丁目", "３０丁目")
    item = item.replace("1丁目", "１丁目")
    item = item.replace("2丁目", "２丁目")
    item = item.replace("3丁目", "３丁目")
    item = item.replace("4丁目", "４丁目")
    item = item.replace("5丁目", "５丁目")
    item = item.replace("6丁目", "６丁目")
    item = item.replace("7丁目", "７丁目")
    item = item.replace("8丁目", "８丁目")
    item = item.replace("9丁目", "９丁目")

    if sapporo:
        item = item.replace("10条", "十条")
        item = item.replace("11条", "十一条")
        item = item.replace("12条", "十二条")
        item = item.replace("13条", "十三条")
        for i in range(1, 10):
            item = item.replace(f"{i}条", f"{i}条".translate(str.maketrans("123456789", "一二三四五六七八九")))

    if asahikawa:
        item = item.replace("十一条", "１１条")
        item = item.replace("十二条", "１２条")
        item = item.replace("十三条", "１３条")
        item = item.replace("十四条", "１４条")
        item = item.replace("十五条", "１５条")
        item = item.replace("十六条", "１６条")
        item = item.replace("十七条", "１７条")
        item = item.replace("十八条", "１８条")
        item = item.replace("十九条", "１９条")
        item = item.replace("二十条", "２０条")
        item = item.replace("一条", "１条")
        item = item.replace("二条", "２条")
        item = item.replace("三条", "３条")
        item = item.replace("四条", "４条")
        item = item.replace("五条", "５条")
        item = item.replace("六条", "６条")
        item = item.replace("七条", "７条")
        item = item.replace("八条", "８条")
        item = item.replace("九条", "９条")
        item = item.replace("十条", "１０条")
      # 替换单独的数字
    
    item = item.replace("10", "１０丁目")
    item = item.replace("11", "１１丁目")
    item = item.replace("12", "１２丁目")
    item = item.replace("13", "１３丁目")
    item = item.replace("14", "１４丁目")
    item = item.replace("15", "１５丁目")
    item = item.replace("16", "１６丁目")
    item = item.replace("17", "１７丁目")
    item = item.replace("18", "１８丁目")
    item = item.replace("19", "１９丁目")
    item = item.replace("20", "２０丁目")
    item = item.replace("21", "２１丁目")
    item = item.replace("22", "２２丁目")
    item = item.replace("23", "２３丁目")
    item = item.replace("24", "２４丁目")
    item = item.replace("25", "２５丁目")
    item = item.replace("26", "２６丁目")
    item = item.replace("27", "２７丁目")
    item = item.replace("28", "２８丁目")
    item = item.replace("29", "２９丁目")
    item = item.replace("30", "３０丁目")
    item = item.replace("1", "１丁目")
    item = item.replace("2", "２丁目")
    item = item.replace("3", "３丁目")
    item = item.replace("4", "４丁目")
    item = item.replace("5", "５丁目")
    item = item.replace("6", "６丁目")
    item = item.replace("7", "７丁目")
    item = item.replace("8", "８丁目")
    item = item.replace("9", "９丁目")

    if sakai:
        item = item.replace("十一丁", "１１丁")
        item = item.replace("十二丁", "１２丁")
        item = item.replace("十三丁", "１３丁")
        item = item.replace("十四丁", "１４丁")
        item = item.replace("十五丁", "１５丁")
        item = item.replace("十六丁", "１６丁")
        item = item.replace("十七丁", "１７丁")
        item = item.replace("十八丁", "１８丁")
        item = item.replace("十九丁", "１９丁")
        item = item.replace("一丁", "１丁")
        item = item.replace("二丁", "２丁")
        item = item.replace("三丁", "３丁")
        item = item.replace("四丁", "４丁")
        item = item.replace("五丁", "５丁")
        item = item.replace("六丁", "６丁")
        item = item.replace("七丁", "７丁")
        item = item.replace("八丁", "８丁")
        item = item.replace("九丁", "９丁")
        item = item.replace("十丁", "１０丁")

    return item