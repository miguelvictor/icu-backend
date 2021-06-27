from django.utils.translation import ugettext_lazy as _

GENDER_CHOICES = (
    ("M", _("Male")),
    ("F", _("Female")),
)
MARITAL_STATUS_CHOICES = (
    ("single", _("Single")),
    ("married", _("Married")),
    ("widowed", _("Widowed")),
    ("divorced", _("Divorced")),
)
ETHNICITY_CHOICES = (
    ("汉族", "汉族"),
    ("满族", "满族"),
    ("蒙古族", "蒙古族"),
    ("回族", "回族"),
    ("藏族", "藏族"),
    ("维吾尔族", "维吾尔族"),
    ("苗族", "苗族"),
    ("彝族", "彝族"),
    ("壮族", "壮族"),
    ("布依族", "布依族"),
    ("侗族", "侗族"),
    ("瑶族", "瑶族"),
    ("白族", "白族"),
    ("土家族", "土家族"),
    ("哈尼族", "哈尼族"),
    ("哈萨克族", "哈萨克族"),
    ("傣族", "傣族"),
    ("黎族", "黎族"),
    ("傈僳族", "傈僳族"),
    ("佤族", "佤族"),
    ("畲族", "畲族"),
    ("高山族", "高山族"),
    ("拉祜族", "拉祜族"),
    ("水族", "水族"),
    ("东乡族", "东乡族"),
    ("纳西族", "纳西族"),
    ("景颇族", "景颇族"),
    ("柯尔克孜族", "柯尔克孜族"),
    ("土族", "土族"),
    ("达斡尔族", "达斡尔族"),
    ("仫佬族", "仫佬族"),
    ("羌族", "羌族"),
    ("布朗族", "布朗族"),
    ("撒拉族", "撒拉族"),
    ("毛南族", "毛南族"),
    ("仡佬族", "仡佬族"),
    ("锡伯族", "锡伯族"),
    ("阿昌族", "阿昌族"),
    ("普米族", "普米族"),
    ("朝鲜族", "朝鲜族"),
    ("塔吉克族", "塔吉克族"),
    ("怒族", "怒族"),
    ("乌孜别克族", "乌孜别克族"),
    ("俄罗斯族", "俄罗斯族"),
    ("鄂温克族", "鄂温克族"),
    ("德昂族", "德昂族"),
    ("保安族", "保安族"),
    ("裕固族", "裕固族"),
    ("京族", "京族"),
    ("塔塔尔族", "塔塔尔族"),
    ("独龙族", "独龙族"),
    ("鄂伦春族", "鄂伦春族"),
    ("赫哲族", "赫哲族"),
    ("门巴族", "门巴族"),
    ("珞巴族", "珞巴族"),
    ("基诺族", "基诺族"),
    ("white", _("White")),
    ("black/african american", _("Black/African American")),
    ("asian", _("Asian")),
    ("hispanic/latino", _("Hispanic/Latino")),
    ("american indian/alaska native", _("American Indian/Alaska Native")),
    ("unknown", _("Unknown")),
)
POSITION_CHOICES = (
    ("nurse", "医护"),
    ("doctor", "医师"),
    ("dean", "院长"),
)
ADMISSION_TYPE_CHOICES = (
    ("ambulatory observation", _("Ambulatory Observation")),
    ("direct emer.", _("Direct Emergency")),
    ("direct observation", _("Direct Observation")),
    ("elective", _("Elective")),
    ("eu observation", _("EU Observation")),
    ("ew emer.", _("EW Emergency")),
    ("observation admit", _("Observation Admit")),
    ("surgical same day admission", _("Surgical Same Day Admission")),
    ("urgent", _("Urgent")),
)
