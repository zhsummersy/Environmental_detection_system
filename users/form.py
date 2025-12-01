from django import forms

class ImageForm(forms.Form):
    title = forms.CharField(label="标题", widget=forms.TextInput(attrs={'class':'form-control'}), max_length=50)
    author = forms.CharField(label="作者", widget=forms.TextInput(attrs={'class':'form-control'}), max_length=50)
    tags = forms.CharField(label="标签", widget=forms.TextInput(attrs={'class':'form-control'}), max_length=50)
    description = forms.CharField(label="正文", widget=forms.Textarea(attrs={'class':'form-control'}), max_length=300)
    image = forms.FileField(label='上传图片',required=False)

class word(forms.Form):
    author = forms.CharField(label="作者", widget=forms.TextInput(attrs={'class':'form-control'}), max_length=20)   
    content = forms.CharField(label="内容", widget=forms.Textarea(attrs={'class':'form-control'}), max_length=50)