<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>
  <xsl:output method="text"/>

  <xsl:template match="/">
    <xsl:apply-templates select="/system/passwd"/>
  </xsl:template>

  <xsl:template match="passwd">
      <xsl:for-each select="account">
      <xsl:value-of select="@username"/>
      <xsl:text>:</xsl:text>
      <xsl:value-of select="@password"/>
      <xsl:text>:</xsl:text>
      <xsl:value-of select="@uid"/>
      <xsl:text>:</xsl:text>
      <xsl:value-of select="@gid"/>
      <xsl:text>:</xsl:text>
      <xsl:value-of select="@realname"/>
      <xsl:text>:</xsl:text>
      <xsl:value-of select="@homedir"/>
      <xsl:text>:</xsl:text>
      <xsl:value-of select="@shell"/>
      <xsl:text>&#10;</xsl:text>
    </xsl:for-each>
  </xsl:template>
</xsl:stylesheet>
