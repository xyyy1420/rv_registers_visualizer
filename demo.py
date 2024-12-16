from django.shortcuts import render
from django.http import HttpResponse
from django import forms

# 定义字段和位解释
REGISTER_FIELDS = {
    "mstatus": {
        "bits": 64,
        "fields": {
            0: ("WPRI", ""),
            1: ("SIE", ""),
            2: ("WPRI", ""),
            3: ("MIE", ""),
            4: ("WPRI", ""),
            5: ("SPIE", ""),
            6: ("UBE", ""),
            7: ("MPIE", ""),
            8: ("SPP", ""),
            9: ("VS[0]", ""),
            10: ("VS[1]", ""),
            11: ("MPP[0]", ""),
            12: ("MPP[1]", ""),
            13: ("FS[0]", "User Interrupt Enable"),
            14: ("FS[1]", "Supervisor Interrupt Enable"),
            15: ("XS[0]", "Machine Interrupt Enable"),
            16: ("XS[1]", "User Previous Interrupt Enable"),
            17: ("MPRV", "Supervisor Previous Interrupt Enable"),
            18: ("SUM", "Machine Previous Interrupt Enable"),
            19: ("MXR", "Supervisor Previous Privilege"),
            20: ("TVM", "Machine Previous Privilege Bit 0"),
            21: ("TW", "Machine Previous Privilege Bit 1"),
            22: ("TSR", "Floating Point State"),
            23: ("WPRI", "Extension State"),
            24: ("WPRI", "Modify Privilege"),
            25: ("WPRI", "Supervisor User Memory Access"),
            26: ("WPRI", "Make eXecutable Readable"),
            27: ("WPRI", "Make eXecutable Readable"),
            28: ("WPRI", "Make eXecutable Readable"),
            29: ("WPRI", "Make eXecutable Readable"),
            30: ("WPRI", "Make eXecutable Readable"),
            31: ("WPRI", "Make eXecutable Readable"),
            32: ("UXL[0]", "Make eXecutable Readable"),
            33: ("UXL[1]", "Make eXecutable Readable"),
            34: ("SXL[0]", "Make eXecutable Readable"),
            35: ("SXL[1]", "Make eXecutable Readable"),
            36: ("SBE", "Make eXecutable Readable"),
            37: ("MBE", "Make eXecutable Readable"),
            38: ("WPRI", "Make eXecutable Readable"),
            39: ("WPRI", "Make eXecutable Readable"),
            40: ("WPRI", "Make eXecutable Readable"),
            41: ("WPRI", "Make eXecutable Readable"),
            42: ("WPRI", "Make eXecutable Readable"),
            43: ("WPRI", "Make eXecutable Readable"),
            44: ("WPRI", "Make eXecutable Readable"),
            45: ("WPRI", "Make eXecutable Readable"),
            46: ("WPRI", "Make eXecutable Readable"),
            47: ("WPRI", "Make eXecutable Readable"),
            48: ("WPRI", "Make eXecutable Readable"),
            49: ("WPRI", "Make eXecutable Readable"),
            50: ("WPRI", "Make eXecutable Readable"),
            51: ("WPRI", "Make eXecutable Readable"),
            52: ("WPRI", "Make eXecutable Readable"),
            53: ("WPRI", "Make eXecutable Readable"),
            54: ("WPRI", "Make eXecutable Readable"),
            55: ("WPRI", "Make eXecutable Readable"),
            56: ("WPRI", "Make eXecutable Readable"),
            57: ("WPRI", "Make eXecutable Readable"),
            58: ("WPRI", "Make eXecutable Readable"),
            59: ("WPRI", "Make eXecutable Readable"),
            60: ("WPRI", "Make eXecutable Readable"),
            61: ("WPRI", "Make eXecutable Readable"),
            62: ("WPRI", "Make eXecutable Readable"),
            63: ("SD", "Make eXecutable Readable"),
        }
    },
    # 可扩展其他寄存器
}

# 表单定义
class RegisterForm(forms.Form):
    register = forms.ChoiceField(choices=[(reg, reg) for reg in REGISTER_FIELDS.keys()])
    value = forms.CharField(max_length=64, help_text="输入16进制寄存器值，例如 0x1800")

# 解析寄存器值
def parse_register(register, value):
    try:
        reg_info = REGISTER_FIELDS[register]
        bit_count = reg_info["bits"]
        fields = reg_info["fields"]

        # 转换值为二进制
        bin_value = bin(int(value, 16))[2:].zfill(bit_count)
        
        # 解析字段
        parsed_fields = []
        for bit, (name, description) in fields.items():
            parsed_fields.append({
                "bit": bit,
                "name": name,
                "value": bin_value[bit_count - 1 - bit],
                "description": description,
            })

        return parsed_fields
    except Exception as e:
        return str(e)

# 视图函数
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            register = form.cleaned_data['register']
            value = form.cleaned_data['value']
            parsed_fields = parse_register(register, value)
            return render(request, 'register.html', {
                'form': form,
                'parsed_fields': parsed_fields,
                'register': register,
                'value': value,
            })
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

# 模板 (register.html)
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>RISC-V Register Visualizer</title>
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        table, th, td {
            border: 1px solid black;
        }
        th, td {
            padding: 8px;
            text-align: left;
        }
    </style>
</head>
<body>
    <h1>RISC-V Register Visualizer</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">解析</button>
    </form>

    {% if parsed_fields %}
        <h2>解析结果</h2>
        <p>寄存器: {{ register }}</p>
        <p>值: {{ value }}</p>
        <table>
            <tr>
                <th>位</th>
                <th>字段名</th>
                <th>值</th>
                <th>描述</th>
            </tr>
            {% for field in parsed_fields %}
            <tr>
                <td>{{ field.bit }}</td>
                <td>{{ field.name }}</td>
                <td>{{ field.value }}</td>
                <td>{{ field.description }}</td>
            </tr>
            {% endfor %}
        </table>
    {% endif %}
</body>
</html>
"""

# 项目配置
if __name__ == "__main__":
    import os
    from django.core.management import execute_from_command_line
    from django.conf import settings

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    settings.configure(
        DEBUG=True,
        SECRET_KEY='thisisasecretkey',
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=['*'],
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [BASE_DIR],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.request',
                    ],
                },
            },
        ],
    )

    from django.urls import path
    urlpatterns = [
        path('', register_view),
    ]

    # 写入模板
    with open(os.path.join(BASE_DIR, 'register.html'), 'w') as f:
        f.write(TEMPLATE)

    execute_from_command_line(["manage.py", "runserver", "0.0.0.0:8000"])

